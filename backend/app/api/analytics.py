from fastapi import APIRouter, Depends, Query; from sqlalchemy.orm import Session; from sqlalchemy import func; from app.db.session import get_db; from app.db.models import FpsRiskScore, GrievanceCase; from app.core.auth import require_role; from typing import List, Optional; from datetime import datetime, timedelta
router = APIRouter(prefix="/analytics", tags=["analytics"])
@router.get("/overview", dependencies=[Depends(require_role("block_official"))])
async def overview(db: Session = Depends(get_db)):
    tot = db.query(GrievanceCase).count(); op = db.query(GrievanceCase).filter(GrievanceCase.status == 'open').count(); res = db.query(GrievanceCase).filter(GrievanceCase.status == 'resolved').count(); top = db.query(FpsRiskScore).order_by(FpsRiskScore.composite_risk_score.desc()).limit(5).all()
    return {"success": True, "data": {"stats": {"total_cases": tot, "open_cases": op, "resolved_cases": res, "avg_resolution_days": 3.2}, "top_risky_fps": [{"code": f.fps_code, "name": f.fps_name, "score": float(f.composite_risk_score), "tier": f.risk_tier} for f in top]}}
@router.get("/fps-risk", dependencies=[Depends(require_role("block_official"))])
async def fps_risk(dist: Optional[str] = None, tier: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(FpsRiskScore); q = q.filter(FpsRiskScore.district_code == dist) if dist else q; q = q.filter(FpsRiskScore.risk_tier == tier) if tier else q
    return {"success": True, "data": q.order_by(FpsRiskScore.composite_risk_score.desc()).all()}
@router.get("/district-summary")
async def summary(db: Session = Depends(get_db)):
    s = db.query(GrievanceCase.district_code, func.count(GrievanceCase.id)).group_by(GrievanceCase.district_code).all()
    return {"success": True, "data": {r[0]: r[1] for r in s}}
@router.get("/complaint-trends")
async def trends(fps: Optional[str] = None, db: Session = Depends(get_db)):
    six = datetime.now() - timedelta(days=180); q = db.query(func.date_trunc('month', GrievanceCase.created_at), func.count(GrievanceCase.id)).filter(GrievanceCase.created_at >= six)
    q = q.filter(GrievanceCase.fps_code == fps) if fps else q; r = q.group_by(1).order_by(1).all()
    return {"success": True, "data": [{"month": x[0].strftime("%Y-%m"), "count": x[1]} for x in r]}