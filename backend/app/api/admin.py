from fastapi import APIRouter, HTTPException, Depends
from app.core.auth import require_role
from app.db.models import GrievanceCase
from app.db.session import get_db
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/cases")
async def list_cases(
    status: str = None,
    fps_code: str = None,
    db: Session = Depends(get_db),
    token: dict = Depends(require_role("block_official"))
):
    query = db.query(GrievanceCase)
    if status:
        query = query.filter(GrievanceCase.status == status)
    if fps_code:
        query = query.filter(GrievanceCase.fps_code == fps_code)
    cases = query.order_by(GrievanceCase.created_at.desc()).limit(100).all()
    return {"success": True, "data": [
        {"id": str(c.id), "case_number": c.case_number, "status": c.status,
         "fps_code": c.fps_code, "issue_type": c.issue_type,
         "created_at": c.created_at.isoformat() if c.created_at else None}
        for c in cases
    ], "error": None}

@router.patch("/cases/{case_number}/status")
async def update_case_status(
    case_number: str, body: dict,
    db: Session = Depends(get_db),
    token: dict = Depends(require_role("block_official"))
):
    case = db.query(GrievanceCase).filter(GrievanceCase.case_number == case_number).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    valid = ['open','acknowledged','under_investigation','resolved','closed']
    if body.get("status") not in valid:
        raise HTTPException(status_code=400, detail=f"Status must be one of {valid}")
    case.status = body["status"]
    if body.get("resolution_notes"):
        case.resolution_notes = body["resolution_notes"]
    db.commit()
    return {"success": True, "data": {"case_number": case_number, "status": body["status"]}, "error": None}
