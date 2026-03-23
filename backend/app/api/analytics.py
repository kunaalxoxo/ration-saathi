from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from app.core.auth import require_role
from app.services.analytics import calculate_fps_risk_score
from app.db.models import FPSRiskScore
from sqlalchemy.orm import Session
from app.db.session import get_db
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/fps-risk")
async def get_fps_risk(
    district: Optional[str] = Query(None), tier: Optional[str] = Query(None),
    limit: int = Query(100), db: Session = Depends(get_db),
    token: dict = Depends(require_role("block_official"))
):
    try:
        q = db.query(FPSRiskScore)
        if district: q = q.filter(FPSRiskScore.district_code == district)
        if tier:
            if tier not in ['low','medium','high','critical']:
                raise HTTPException(status_code=400, detail="Invalid tier")
            q = q.filter(FPSRiskScore.risk_tier == tier)
        results = q.order_by(FPSRiskScore.composite_risk_score.desc()).limit(limit).all()
        return {"success": True, "data": [
            {"fps_code": f.fps_code, "district_code": f.district_code, "block_code": f.block_code,
             "fps_name": f.fps_name, "complaints_30d": f.complaints_30d,
             "composite_risk_score": float(f.composite_risk_score), "risk_tier": f.risk_tier}
            for f in results
        ], "error": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/district-summary")
async def get_district_summary(
    state: Optional[str] = Query(None), db: Session = Depends(get_db),
    token: dict = Depends(require_role("block_official"))
):
    try:
        from sqlalchemy import text
        q = "SELECT r.district_code, COUNT(DISTINCT r.id), COUNT(g.id) FROM ration_cards r LEFT JOIN grievance_cases g ON r.id=g.ration_card_id WHERE r.is_active=true"
        params = {}
        if state: q += " AND r.state_code=:state"; params["state"] = state
        q += " GROUP BY r.district_code ORDER BY r.district_code"
        rows = db.execute(text(q), params).fetchall()
        return {"success": True, "data": [{"district_code": r[0], "total_ration_cards": r[1], "total_complaints": r[2]} for r in rows], "error": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/complaint-trends")
async def get_complaint_trends(
    fps: Optional[str] = Query(None), months: int = Query(3),
    db: Session = Depends(get_db), token: dict = Depends(require_role("block_official"))
):
    try:
        from sqlalchemy import text
        from datetime import date, timedelta
        start = date.today() - timedelta(days=30*months)
        q = "SELECT TO_CHAR(date_trunc('month',created_at),'YYYY-MM'), COUNT(*) FROM grievance_cases WHERE created_at>=:start"
        params = {"start": start}
        if fps: q += " AND fps_code=:fps"; params["fps"] = fps
        q += " GROUP BY 1 ORDER BY 1"
        rows = db.execute(text(q), params).fetchall()
        return {"success": True, "data": [{"month": r[0], "complaint_count": r[1]} for r in rows], "error": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/overview")
async def get_overview(db: Session = Depends(get_db), token: dict = Depends(require_role("block_official"))):
    try:
        from sqlalchemy import text
        row = db.execute(text("SELECT COUNT(*), SUM(CASE WHEN status='open' THEN 1 ELSE 0 END), SUM(CASE WHEN status IN ('resolved','closed') THEN 1 ELSE 0 END), AVG(CASE WHEN status IN ('resolved','closed') THEN EXTRACT(EPOCH FROM (updated_at-created_at))/86400 ELSE NULL END) FROM grievance_cases")).fetchone()
        top = db.execute(text("SELECT fps_code,fps_name,district_code,composite_risk_score,risk_tier FROM fps_risk_scores ORDER BY composite_risk_score DESC LIMIT 5")).fetchall()
        return {"success": True, "data": {
            "total_cases": row[0] or 0, "open_cases": row[1] or 0,
            "resolved_cases": row[2] or 0,
            "avg_resolution_days": round(float(row[3]), 2) if row[3] else 0.0,
            "top_risky_fps": [{"fps_code": r[0], "fps_name": r[1], "district_code": r[2], "composite_risk_score": float(r[3]), "risk_tier": r[4]} for r in top]
        }, "error": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
