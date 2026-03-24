from fastapi import APIRouter, Depends, HTTPException; from sqlalchemy.orm import Session; from app.db.session import get_db; from app.db.models import User; from app.core.encryption import encryption_service; from app.core.auth import generate_and_store_otp, create_access_token, redis; from pydantic import BaseModel
router = APIRouter(prefix="/auth", tags=["auth"])
class OTPRequest(BaseModel): phone: str
class OTPVerify(BaseModel): phone: str; otp: str
@router.post("/request-otp")
async def request_otp(d: OTPRequest, db: Session = Depends(get_db)):
    h = encryption_service.hash_for_lookup(d.phone); u = db.query(User).filter(User.phone_hash == h).first()
    if not u: raise HTTPException(status_code=404); otp = await generate_and_store_otp(h)
    print(f"DEMO OTP for {d.phone}: {otp}"); return {"success": True}
@router.post("/verify-otp")
async def verify_otp(d: OTPVerify, db: Session = Depends(get_db)):
    h = encryption_service.hash_for_lookup(d.phone); s_o = redis.get(f"otp:{h}")
    if not s_o or s_o != d.otp: raise HTTPException(status_code=401)
    u = db.query(User).filter(User.phone_hash == h).first(); redis.delete(f"otp:{h}")
    return {"success": True, "token": create_access_token({"sub": str(u.id), "role": u.role, "district_code": u.district_code})}
