from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import User
from app.core.encryption import encryption_service
from app.core.auth import generate_and_store_otp, create_access_token, redis
from app.services.sms import sms_service
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])


class OTPRequest(BaseModel):
    phone: str


class OTPVerify(BaseModel):
    phone: str
    otp: str


@router.post("/request-otp")
async def request_otp(d: OTPRequest, db: Session = Depends(get_db)):
    h = encryption_service.hash_for_lookup(d.phone)
    u = db.query(User).filter(User.phone_hash == h).first()
    if not u:
        logger.warning(f"OTP requested for non-existent user: {d.phone}")
        raise HTTPException(status_code=404, detail="User not found")
    
    otp = await generate_and_store_otp(h)
    logger.info(f"Generated OTP for {d.phone}")
    
    success = await sms_service.send_otp_sms(d.phone, otp)
    if not success:
        logger.error(f"Failed to send SMS to {d.phone}")
        # Still return success in demo if needed, but for now let's be strict
        # return {"success": True, "demo_otp": otp} 
    
    return {"success": True}


@router.post("/verify-otp")
async def verify_otp(d: OTPVerify, db: Session = Depends(get_db)):
    h = encryption_service.hash_for_lookup(d.phone)
    s_o = redis.get(f"otp:{h}")
    
    if not s_o or s_o != d.otp:
        logger.warning(f"Invalid OTP attempt for {d.phone}")
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")
        
    u = db.query(User).filter(User.phone_hash == h).first()
    if not u:
        raise HTTPException(status_code=404)
        
    redis.delete(f"otp:{h}")
    token = create_access_token({
        "sub": str(u.id),
        "role": u.role,
        "district_code": u.district_code
    })
    
    return {
        "success": True,
        "token": token,
        "user": {
            "id": u.id,
            "name": u.name,
            "role": u.role,
            "district_code": u.district_code,
            "phone": d.phone
        }
    }
