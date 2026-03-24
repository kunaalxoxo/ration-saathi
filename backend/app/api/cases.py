from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import GrievanceCase
from pydantic import BaseModel 

router = APIRouter(prefix="/cases", tags=["cases"])

class CaseStatusResponse(BaseModel):
    case_number: str
    status: str
    created_at: str
    issue_type: str

@router.get("/{cn}", response_model=CaseStatusResponse)
async def get_status(cn: str, db: Session = Depends(get_db)):
    case = db.query(GrievanceCase).filter(GrievanceCase.case_number == cn).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return {
        "case_number": case.case_number, 
        "status": case.status, 
        "created_at": case.created_at.isoformat(), 
        "issue_type": case.issue_type
    }

@router.post("/ivr-status")
async def ivr_status(digits: str, db: Session = Depends(get_db)):
    cn = f"RS-RJ-2025-{int(digits):05d}"
    case = db.query(GrievanceCase).filter(GrievanceCase.case_number == cn).first()
    if case:
        return {"success": True, "status": case.status, "prompt": f"Aapka case {case.status} hai."}
    else:
        return {"success": False, "prompt": "Case number nahi mila."}
