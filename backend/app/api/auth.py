from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.encryption import hash_for_lookup
from app.core.auth import generate_otp, store_otp, verify_otp, check_otp_rate_limit, create_access_token
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class OTPRequest(BaseModel):
    phone_number: str

class OTPVerify(BaseModel):
    phone_number: str
    otp: str

@router.post("/request-otp")
async def request_otp(body: OTPRequest):
    phone_hash = hash_for_lookup(body.phone_number)
    if not await check_otp_rate_limit(phone_hash):
        raise HTTPException(status_code=429, detail="Too many requests. Wait 15 minutes.")
    otp = generate_otp()
    await store_otp(phone_hash, otp)
    logger.info("OTP for demo: %s", otp)
    return {"success": True, "data": {"message": "OTP sent"}, "error": None}

@router.post("/verify-otp")
async def verify_otp_endpoint(body: OTPVerify):
    phone_hash = hash_for_lookup(body.phone_number)
    if not await verify_otp(phone_hash, body.otp):
        raise HTTPException(status_code=401, detail="Invalid or expired OTP")
    token = create_access_token({"sub": phone_hash, "phone_hash": phone_hash, "role": "csc_operator"})
    return {"success": True, "data": {"access_token": token, "token_type": "bearer"}, "error": None}
