from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.core.config import settings
from upstash_redis import Redis
import secrets

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")
redis = Redis(url=settings.UPSTASH_REDIS_REST_URL, token=settings.UPSTASH_REDIS_REST_TOKEN)

ROLE_HIERARCHY = {
    "csc_operator": 1,
    "shg_leader": 1,
    "block_official": 2,
    "district_admin": 3,
    "state_admin": 4,
    "super_admin": 5
}

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        p = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        u_id = p.get("sub")
        r = p.get("role")
        if u_id is None or r is None:
            raise HTTPException(status_code=401)
        return {"user_id": u_id, "role": r, "district": p.get("district_code")}
    except JWTError:
        raise HTTPException(status_code=401)

def require_role(r_role: str):
    async def checker(c_user: dict = Depends(get_current_user)):
        if ROLE_HIERARCHY.get(c_user["role"], 0) < ROLE_HIERARCHY.get(r_role, 99):
            raise HTTPException(status_code=403)
        return c_user
    return checker

async def generate_and_store_otp(p_hash: str) -> str:
    key = f"rate:otp:{p_hash}"
    att = redis.incr(key)
    if att == 1:
        redis.expire(key, 900)
    elif att > 3:
        raise HTTPException(status_code=429)
    otp = "".join(str(secrets.randbelow(10)) for _ in range(6))
    redis.set(f"otp:{p_hash}", otp, ex=300)
    return otp
