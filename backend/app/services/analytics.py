try:
    import duckdb
except ImportError:
    duckdb = None

from typing import Dict, Any
from datetime import date, timedelta
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


def calculate_fps_risk_score(fps_code: str) -> Dict[str, Any]:
    default_return = {
        "fps_code": fps_code, "district_code": None, "block_code": None,
        "fps_name": None, "complaints_30d": 0, "complaints_90d": 0,
        "resolution_rate": 100.0, "pos_anomaly_score": 0.0,
        "repeat_complaint_rate": 0.0, "composite_risk_score": 0.0,
        "risk_tier": "low", "last_calculated_at": date.today()
    }
    if duckdb is None:
        logger.warning("DuckDB not installed - returning default for %s", fps_code)
        return default_return
    try:
        from urllib.parse import urlparse
        url = urlparse(settings.DATABASE_URL)
        con = duckdb.connect(':memory:')
        con.execute("INSTALL postgres; LOAD postgres;")
        con.execute(f"ATTACH 'host={url.hostname} user={url.username} password={url.password} dbname={url.path[1:]} port={url.port}' AS pg (TYPE POSTGRES);")
        con.execute("SET search_path = pg.public;")

        r1 = con.execute("SELECT district_code, block_code, household_head_name FROM ration_cards WHERE fps_code=? AND is_active=true LIMIT 1", [fps_code]).fetchone()
        total = con.execute("SELECT COUNT(*) FROM ration_cards WHERE fps_code=? AND is_active=true", [fps_code]).fetchone()[0] or 0
        t30, t90 = date.today() - timedelta(30), date.today() - timedelta(90)
        r3 = con.execute("SELECT SUM(CASE WHEN created_at>=? THEN 1 ELSE 0 END), SUM(CASE WHEN created_at>=? THEN 1 ELSE 0 END) FROM grievance_cases WHERE fps_code=?", [t30,t90,fps_code]).fetchone()
        r4 = con.execute("SELECT COUNT(*), SUM(CASE WHEN status IN ('resolved','closed') THEN 1 ELSE 0 END) FROM grievance_cases WHERE fps_code=?", [fps_code]).fetchone()
        r5 = con.execute("SELECT SUM(rice_kg+wheat_kg), SUM(COALESCE(actual_offtake_rice,0)+COALESCE(actual_offtake_wheat,0)) FROM monthly_allocations WHERE fps_code=? AND month_year=(SELECT MAX(month_year) FROM monthly_allocations WHERE fps_code=?)", [fps_code,fps_code]).fetchone()
        r6 = con.execute("SELECT reporter_phone_encrypted, COUNT(*) FROM grievance_cases WHERE fps_code=? AND created_at>=? GROUP BY reporter_phone_encrypted", [fps_code,t30]).fetchall()
        con.close()

        c30, c90 = r3[0] or 0, r3[1] or 0
        tot_cases, resolved = r4[0] or 0, r4[1] or 0
        allocated, actual = (r5[0] or 0), (r5[1] or 0)
        repeat = sum(row[1] for row in (r6 or []) if row[1] > 1)

        c30r = (c30/total*100) if total > 0 else 0.0
        c90r = (c90/total*100) if total > 0 else 0.0
        res_rate = (resolved/tot_cases*100) if tot_cases > 0 else 100.0
        pos = max(0.0, 1 - actual/allocated)*100 if allocated > 0 else 0.0
        rep = (repeat/c30*100) if c30 > 0 else 0.0
        score = max(0.0, min(100.0, c30r*0.30 + c90r*0.15 + (100-res_rate)*0.20 + pos*0.25 + rep*0.10))
        tier = "critical" if score >= 75 else "high" if score >= 50 else "medium" if score >= 25 else "low"

        return {
            "fps_code": fps_code, "district_code": r1[0] if r1 else None,
            "block_code": r1[1] if r1 else None, "fps_name": r1[2] if r1 else None,
            "complaints_30d": int(c30), "complaints_90d": int(c90),
            "resolution_rate": round(res_rate, 2), "pos_anomaly_score": round(pos, 2),
            "repeat_complaint_rate": round(rep, 2), "composite_risk_score": round(score, 2),
            "risk_tier": tier, "last_calculated_at": date.today()
        }
    except Exception as e:
        logger.error("Risk score error for %s: %s", fps_code, str(e))
        return default_return


async def update_fps_risk_score(fps_code: str) -> None:
    try:
        score = calculate_fps_risk_score(fps_code)
        logger.info("Updated risk score for %s: %.1f (%s)", fps_code, score["composite_risk_score"], score["risk_tier"])
    except Exception as e:
        logger.error("Failed to update risk score for %s: %s", fps_code, str(e))
