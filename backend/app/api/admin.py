from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import GrievanceCase
from app.core.auth import require_role
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/admin", tags=["admin"])


class GrievanceUpdate(BaseModel):
    status: str
    resolution_notes: Optional[str] = None


@router.get("/cases", dependencies=[Depends(require_role("block_official"))])
async def list_cases(
    status: Optional[str] = None,
    fps_code: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Admin endpoint to list and filter all grievance cases."""
    query = db.query(GrievanceCase)
    if status:
        query = query.filter(GrievanceCase.status == status)
    if fps_code:
        query = query.filter(GrievanceCase.fps_code == fps_code)

    return {"success": True, "data": query.order_by(GrievanceCase.created_at.desc()).all()}


@router.patch("/cases/{case_id}", dependencies=[Depends(require_role("block_official"))])
async def update_case_status(
    case_id: str,
    data: GrievanceUpdate,
    db: Session = Depends(get_db)
):
    """Updates status and notes for a grievance."""
    case = db.query(GrievanceCase).filter(GrievanceCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    case.status = data.status # type: ignore
    if data.resolution_notes:
        case.resolution_notes = data.resolution_notes # type: ignore

    db.commit()
    return {"success": True, "message": "Case updated"}
