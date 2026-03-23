# FILE: ration-saathi/backend/app/api/analytics.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from app.core.auth import verify_token, require_role
from app.services.analytics import calculate_fps_risk_score
from app.db.models import FPSRiskScore
from sqlalchemy.orm import Session
from app.db.session import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/fps-risk")
async def get_fps_risk(
    district: Optional[str] = Query(None, description="Filter by district code"),
    tier: Optional[str] = Query(None, description="Filter by risk tier (low, medium, high, critical)"),
    limit: int = Query(100, description="Maximum number of results to return"),
    db: Session = Depends(get_db),
    token: dict = Depends(require_role("block_official"))  # block_official or above
):
    """
    Get list of FPS with risk scores, optionally filtered by district and tier.
    Requires block_official role or above.
    """
    try:
        query = db.query(FPSRiskScore)
        
        if district:
            query = query.filter(FPSRiskScore.district_code == district)
        
        if tier:
            if tier not in ['low', 'medium', 'high', 'critical']:
                raise HTTPException(status_code=400, detail="Invalid tier. Must be one of: low, medium, high, critical")
            query = query.filter(FPSRiskScore.risk_tier == tier)
        
        results = query.order_by(FPSRiskScore.composite_risk_score.desc()).limit(limit).all()
        
        # Convert to list of dictionaries
        fps_list = []
        for fps in results:
            fps_list.append({
                "fps_code": fps.fps_code,
                "district_code": fps.district_code,
                "block_code": fps.block_code,
                "fps_name": fps.fps_name,
                "complaints_30d": fps.complaints_30d,
                "complaints_90d": fps.complaints_90d,
                "resolution_rate": float(fps.resolution_rate),
                "pos_anomaly_score": float(fps.pos_anomaly_score),
                "composite_risk_score": float(fps.composite_risk_score),
                "risk_tier": fps.risk_tier,
                "last_calculated_at": fps.last_calculated_at.isoformat() if fps.last_calculated_at else None
            })
        
        return {
            "success": True,
            "data": fps_list,
            "error": None
        }
        
    except Exception as e:
        logger.error(f"Error fetching FPS risk data: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/district-summary")
async def get_district_summary(
    state: Optional[str] = Query(None, description="Filter by state code"),
    db: Session = Depends(get_db),
    token: dict = Depends(require_role("block_official"))  # block_official or above
):
    """
    Get per-district complaint count, avg resolution rate, critical FPS count.
    Requires block_official role or above.
    """
    try:
        # We'll use raw SQL for this complex query
        from sqlalchemy import text
        
        query = """
            SELECT 
                r.district_code,
                COUNT(DISTINCT r.id) as total_ration_cards,
                COUNT(g.id) as total_complaints,
                ROUND(AVG(CASE WHEN g.status IN ('resolved', 'closed') THEN 1.0 ELSE 0.0 END) * 100, 2) as avg_resolution_rate,
                SUM(CASE WHEN f.risk_tier = 'critical' THEN 1 ELSE 0 END) as critical_fps_count
            FROM ration_cards r
            LEFT JOIN grievance_cases g ON r.id = g.ration_card_id
            LEFT JOIN fps_risk_scores f ON r.fps_code = f.fps_code
            WHERE r.is_active = true
        """
        
        params = {}
        if state:
            query += " AND r.state_code = :state"
            params["state"] = state
        
        query += " GROUP BY r.district_code ORDER BY r.district_code"
        
        results = db.execute(text(query), params).fetchall()
        
        # Convert to list of dictionaries
        district_list = []
        for row in results:
            district_list.append({
                "district_code": row[0],
                "total_ration_cards": row[1],
                "total_complaints": row[2],
                "avg_resolution_rate": float(row[3]) if row[3] is not None else 0.0,
                "critical_fps_count": row[4]
            })
        
        return {
            "success": True,
            "data": district_list,
            "error": None
        }
        
    except Exception as e:
        logger.error(f"Error fetching district summary: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/complaint-trends")
async def get_complaint_trends(
    fps: Optional[str] = Query(None, description="Filter by FPS code"),
    months: int = Query(3, description="Number of months to look back (default: 3)"),
    db: Session = Depends(get_db),
    token: dict = Depends(require_role("block_official"))  # block_official or above
):
    """
    Get monthly complaint counts for chart.js line chart.
    Requires block_official role or above.
    """
    try:
        from sqlalchemy import text
        from datetime import date, timedelta
        
        # Calculate the start date
        end_date = date.today()
        start_date = end_date - timedelta(days=30 * months)
        
        query = """
            SELECT 
                TO_CHAR(date_trunc('month', g.created_at), 'YYYY-MM') as month,
                COUNT(g.id) as complaint_count
            FROM grievance_cases g
            JOIN ration_cards r ON g.ration_card_id = r.id
            WHERE g.created_at >= :start_date
        """
        
        params = {"start_date": start_date}
        
        if fps:
            query += " AND r.fps_code = :fps"
            params["fps"] = fps
        
        query += " GROUP BY date_trunc('month', g.created_at) ORDER BY date_trunc('month', g.created_at)"
        
        results = db.execute(text(query), params).fetchall()
        
        # Convert to list of dictionaries
        trends = []
        for row in results:
            trends.append({
                "month": row[0],
                "complaint_count": row[1]
            })
        
        return {
            "success": True,
            "data": trends,
            "error": None
        }
        
    except Exception as e:
        logger.error(f"Error fetching complaint trends: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/overview")
async def get_overview(
    db: Session = Depends(get_db),
    token: dict = Depends(require_role("block_official"))  # block_official or above
):
    """
    Get overall statistics: total cases, open cases, resolved cases, avg resolution time, top 5 risky FPS.
    Requires block_official role or above.
    """
    try:
        from sqlalchemy import text
        
        # Get overall case statistics
        case_stats_query = """
            SELECT 
                COUNT(*) as total_cases,
                SUM(CASE WHEN status = 'open' THEN 1 ELSE 0 END) as open_cases,
                SUM(CASE WHEN status IN ('resolved', 'closed') THEN 1 ELSE 0 END) as resolved_cases,
                AVG(CASE WHEN status IN ('resolved', 'closed') 
                    THEN EXTRACT(EPOCH FROM (updated_at - created_at)) / 86400  -- Convert seconds to days
                    ELSE NULL END) as avg_resolution_days
            FROM grievance_cases
        """
        
        case_results = db.execute(text(case_stats_query)).fetchone()
        
        # Get top 5 risky FPS
        top_risky_query = """
            SELECT 
                f.fps_code,
                f.fps_name,
                f.district_code,
                f.block_code,
                f.composite_risk_score,
                f.risk_tier
            FROM fps_risk_scores f
            ORDER BY f.composite_risk_score DESC
            LIMIT 5
        """
        
        top_risky_results = db.execute(text(top_risky_query)).fetchall()

        # Format the results
        overview = {
            "total_cases": case_results[0] if case_results else 0,
            "open_cases": case_results[1] if case_results else 0,
            "resolved_cases": case_results[2] if case_results else 0,
            "avg_resolution_days": round(float(case_results[3]), 2) if case_results and case_results[3] is not None else 0.0,
            "top_risky_fps": []
        }
        
        for row in top_risky_results:
            overview["top_risky_fps"].append({
                "fps_code": row[0],
                "fps_name": row[1],
                "district_code": row[2],
                "block_code": row[3],
                "composite_risk_score": float(row[4]),
                "risk_tier": row[5]
            })
        
        return {
            "success": True,
            "data": overview,
            "error": None
        }
        
    except Exception as e:
        logger.error(f"Error fetching overview: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
