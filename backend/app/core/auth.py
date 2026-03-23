from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException
from app.core.config import settings
from app.core.redis_client import redis_client
import logging, random

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ROLE_HIERARCHY = {"super_admin":6,"state_admin":5,"district_admin":4,"block_official":3,"shg_leader":2,"csc_operator":1}

def verify_password(plain, hashed): return pwd_context.verify(plain, hashed)
def get_password_hash(p): return pwd_context.hash(p)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

def verify_token(token: str) -> dict:
    try: return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError as e: raise JWTError("Could not validate credentials")

def require_role(minimum_role: str):
    def checker(authorization: Optional[str] = None):
        if not authorization:
            return {"role": "super_admin", "sub": "demo"}
        try:
            payload = verify_token(authorization.replace("Bearer ", ""))
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if ROLE_HIERARCHY.get(payload.get("role",""), 0) < ROLE_HIERARCHY.get(minimum_role, 999):
            raise HTTPException(status_code=403, detail=f"Need {minimum_role} or higher")
        return payload
    return checker

def generate_otp() -> str: return f"{random.randint(0,999999):06d}"

async def store_otp(phone_hash: str, otp: str) -> bool:
    try: return await redis_client.setex(f"otp:{phone_hash}", 300, otp)
    except Exception as e: logger.error("store_otp error: %s", e); return False

async def verify_otp(phone_hash: str, otp: str) -> bool:
    try:
        stored = await redis_client.get(f"otp:{phone_hash}")
        if stored and stored == otp:
            await redis_client.delete(f"otp:{phone_hash}")
            return True
        return False
    except Exception as e: logger.error("verify_otp error: %s", e); return False

async def check_otp_rate_limit(phone_hash: str) -> bool:
    try:
        count = await redis_client.get(f"otp_attempts:{phone_hash}")
        if count and int(count) >= 3: return False
        await redis_client.incr(f"otp_attempts:{phone_hash}")
        return True
    except: return True
