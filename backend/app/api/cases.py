from fastapi import APIRouter, HTTPException, Depends
from app.db.models import GrievanceCase
from app.db.session import get_db
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/{case_number}/status")
async def get_case_status(case_number: str, db: Session = Depends(get_db)):
    case = db.query(GrievanceCase).filter(GrievanceCase.case_number == case_number).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return {"success": True, "data": {
        "case_number": case.case_number,
        "status": case.status,
        "issue_type": case.issue_type,
        "fps_code": case.fps_code,
        "resolution_notes": case.resolution_notes,
        "created_at": case.created_at.isoformat() if case.created_at else None
    }, "error": None}

@router.post("/create")
async def create_case_web(request_data: dict, db: Session = Depends(get_db)):
    from app.services.grievance import create_grievance_case
    result = await create_grievance_case(request_data)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
