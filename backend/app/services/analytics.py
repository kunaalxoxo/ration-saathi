# FILE: ration-saathi/backend/app/services/analytics.py
import logging
from typing import Dict, Any, Optional
from datetime import date, timedelta

try:
    import duckdb
except ImportError:
    duckdb = None

logger = logging.getLogger(__name__)

# Default return value in case of error or missing duckdb
default_return = {
    "fps_code": None,
    "district_code": None,
    "block_code": None,
    "fps_name": None,
    "complaints_30d": 0,
    "complaints_90d": 0,
    "resolution_rate": 100.0,  # Default to 100% (no risk)
    "pos_anomaly_score": 0.0,
    "repeat_complaint_rate": 0.0,
    "composite_risk_score": 0.0,
    "risk_tier": "low",
    "last_calculated_at": date.today()
}

def calculate_fps_risk_score(fps_code: str) -> Dict[str, Any]:
    """
    Calculate the FPS risk score based on the five components.
    Returns a dictionary with the score components and the overall score.
    If duckdb is not available, returns a default score.
    """
    if duckdb is None:
        logger.error("DuckDB is not installed. Returning default risk score for FPS: %s", fps_code)
        return default_return

    # Default return value in case of error
    # (We keep the same structure as default_return but we'll overwrite with actual values if possible)
    result = default_return.copy()
    result["fps_code"] = fps_code

    try:
        # Parse the DATABASE_URL to get connection parameters
        from urllib.parse import urlparse
        from app.core.config import settings
        url = urlparse(settings.DATABASE_URL)
        dbname = url.path[1:]  # remove the leading '/'
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port

        # Create an in-memory DuckDB connection
        con = duckdb.connect(database=':memory:', read_only=False)

        # Install and load the postgres extension
        con.execute("INSTALL postgres;")
        con.execute("LOAD postgres;")

        # Attach the PostgreSQL database
        attach_string = f"host='{host}' user='{user}' password='{password}' dbname='{dbname}' port={port}"
        con.execute(f"ATTACH '{attach_string}' AS postgres_db (TYPE POSTGRES);")

        # Set the search path to include the attached database for convenience
        con.execute("SET search_path = postgres_db.public;")

        # Query 1: Get district_code, block_code, fps_name from ration_cards for the given fps_code (limit 1)
        query1 = """
            SELECT district_code, block_code, household_head_name as fps_name
            FROM ration_cards
            WHERE fps_code = ? AND is_active = true
            LIMIT 1
        """
        result1 = con.execute(query1, [fps_code]).fetchone()
        if result1:
            district_code, block_code, fps_name = result1
            result["district_code"] = district_code
            result["block_code"] = block_code
            result["fps_name"] = fps_name
        else:
            # If no active ration cards, we still want to calculate the score based on other data
            # Leave as None (already set in default_return)
            pass

        # Query 2: Get total_ration_cards (active) for the fps_code
        query2 = """
            SELECT COUNT(*)
            FROM ration_cards
            WHERE fps_code = ? AND is_active = true
        """
        total_ration_cards = con.execute(query2, [fps_code]).fetchone()[0]

        # Query 3: Get complaints_30d and complaints_90d for the fps_code
        thirty_days_ago = date.today() - timedelta(days=30)
        ninety_days_ago = date.today() - timedelta(days=90)
        query3 = """
            SELECT 
                SUM(CASE WHEN created_at >= ? THEN 1 ELSE 0 END) as complaints_30d,
                SUM(CASE WHEN created_at >= ? THEN 1 ELSE 0 END) as complaints_90d
            FROM grievance_cases
            WHERE fps_code = ?
        """
        result3 = con.execute(query3, [thirty_days_ago, ninety_days_ago, fps_code]).fetchone()
        complaints_30d = result3[0] if result3 else 0
        complaints_90d = result3[1] if result3 else 0
        result["complaints_30d"] = int(complaints_30d)
        result["complaints_90d"] = int(complaints_90d)

        # Query 4: Get total_cases and resolved_cases for the fps_code
        query4 = """
            SELECT 
                COUNT(*) as total_cases,
                SUM(CASE WHEN status IN ('resolved', 'closed') THEN 1 ELSE 0 END) as resolved_cases
            FROM grievance_cases
            WHERE fps_code = ?
        """
        result4 = con.execute(query4, [fps_code]).fetchone()
        total_cases = result4[0] if result4 else 0
        resolved_cases = result4[1] if result4 else 0

        # Query 5: Get the most recent month_year for the fps_code in monthly_allocations, 
        # then get the total allocated and actual offtake for that month.
        query5 = """
            SELECT 
                SUM(rice_kg + wheat_kg) as total_allocated,
                SUM(COALESCE(actual_offtake_rice, 0) + COALESCE(actual_offtake_wheat, 0)) as total_actual
            FROM monthly_allocations
            WHERE fps_code = ?
            AND month_year = (
                SELECT MAX(month_year)
                FROM monthly_allocations
                WHERE fps_code = ?
            )
        """
        result5 = con.execute(query5, [fps_code, fps_code]).fetchone()
        total_allocated = result5[0] if result5 and result5[0] is not None else 0
        total_actual = result5[1] if result5 and result5[1] is not None else 0

        # Query 6: Get the complaints in the last 30 days for the fps_code with the reporter's phone_encrypted
        # to compute repeat_complaint_rate.
        query6 = """
            SELECT reporter_phone_encrypted, COUNT(*) as complaint_count
            FROM grievance_cases
            WHERE fps_code = ? AND created_at >= ?
            GROUP BY reporter_phone_encrypted
        """
        results6 = con.execute(query6, [fps_code, thirty_days_ago]).fetchall()
        total_complaints_30d = complaints_30d  # from query3
        repeat_complaints = 0
        if results6:
            for row in results6:
                if row[1] > 1:  # more than one complaint from this reporter
                    repeat_complaints += row[1]

        # Close the DuckDB connection
        con.close()

        # Now calculate the components

        # Component 1: complaints_30d_rate (percentage)
        if total_ration_cards > 0:
            complaints_30d_rate = (complaints_30d / total_ration_cards) * 100
        else:
            complaints_30d_rate = 0.0
        result["complaints_30d_rate"] = complaints_30d_rate  # Not in final return, but we can keep for debugging if needed

        # Component 2: complaints_90d_rate (percentage)
        if total_ration_cards > 0:
            complaints_90d_rate = (complaints_90d / total_ration_cards) * 100
        else:
            complaints_90d_rate = 0.0

        # Component 3: resolution_rate (percentage of resolved cases) -> we use (100 - resolution_rate) for risk
        if total_cases > 0:
            resolution_rate = (resolved_cases / total_cases) * 100
        else:
            resolution_rate = 100.0  # No cases, so no risk from unresolved cases
        # For the risk score, we use (100 - resolution_rate) so that low resolution rate gives high risk
        resolution_risk = 100.0 - resolution_rate

        # Component 4: pos_anomaly_score (percentage of shortfall, but only if actual < 85% of allocated)
        if total_allocated > 0:
            actual_allocated_ratio = total_actual / total_allocated
            # If actual > allocated, ratio > 1, then shortfall is negative -> we set to 0 (no risk from over-supply)
            if actual_allocated_ratio > 1:
                pos_anomaly = 0.0
            else:
                pos_anomaly = 1 - actual_allocated_ratio  # fraction of shortfall
            # Only consider it an anomaly if actual_allocated_ratio < 0.85 (i.e., pos_anomaly > 0.15)
            # But we'll use the pos_anomaly as is (0 to 1) and then multiply by 100 to get a percentage for
