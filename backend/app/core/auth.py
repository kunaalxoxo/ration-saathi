# FILE: ration-saathi/backend/app/core/auth.py
from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.db.models import User
from sqlalchemy.orm import Session
from app.db.session import get_db
import logging

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Role hierarchy for access control
ROLE_HIERARCHY = {
    "super_admin": 6,
    "state_admin": 5,
    "district_admin": 4,
    "block_official": 3,
    "shg_leader": 2,
    "csc_operator": 1,
}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token
    Returns the payload if valid, raises JWTError if invalid
    """
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError as e:
        logger.error(f"JWT verification failed: {str(e)}")
        raise JWTError("Could not validate credentials")

def get_user_by_phone_hash(db: Session, phone_hash: str) -> Optional[User]:
    """Get user by phone hash"""
    return db.query(User).filter(User.phone_hash == phone_hash).first()

def authenticate_user(db: Session, phone_number: str, password: str) -> Optional[User]:
    """
    Authenticate a user with phone number and password
    Used for admin login (username/password)
    """
    # First, we need to hash the phone number to look up the user
    from app.core.encryption import hash_for_lookup
    phone_hash = hash_for_lookup(phone_number)
    
    user = get_user_by_phone_hash(db, phone_hash)
    if not user:
        return None
    if not verify_password(password, user.phone_encrypted):  # In reality, we'd have a separate password hash
        return None
    return user

def create_user_access_token(user: User) -> str:
    """Create an access token for a user"""
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "phone_hash": user.phone_hash,
            "role": user.role,
            "district_code": user.district_code,
            "block_code": user.block_code
        },
        expires_delta=access_token_expires
    )
    return access_token

def get_current_user(token: str = None, db: Session = None) -> Optional[dict]:
    """
    Get current user from token
    Returns user dict if token is valid
    """
    if not token or not db:
        return None
    try:
        payload = verify_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            return None
        
        # Get user from DB
        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            return None
            
        return {
            "id": str(user.id),
            "phone_hash": user.phone_hash,
            "role": user.role,
            "district_code": user.district_code,
            "block_code": user.block_code,
            "is_active": user.is_active
        }
    except JWTError:
        return None

def require_role(minimum_role: str):
    """
    Dependency factory for role-based access control
    Returns a dependency that checks if the user has at least the minimum role
    """
    def role_checker(token: dict = Depends(verify_token)):
        user_role = token.get("role")
        if not user_role:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        user_level = ROLE_HIERARCHY.get(user_role, 0)
        required_level = ROLE_HIERARCHY.get(minimum_role, 999)  # High number if role not found
        
        if user_level < required_level:
            raise HTTPException(
                status_code=403, 
                detail=f"Insufficient permissions. Required role: {minimum_role} or higher"
            )
        return token
    return role_checker

# OTP functions
def generate_otp() -> str:
    """Generate a 6-digit numeric OTP"""
    import random
    return f"{random.randint(0, 999999):06d}"

async def store_otp(phone_hash: str, otp: str) -> bool:
    """
    Store OTP in Redis with 5-minute TTL
    Returns True if successful
    """
    try:
        key = f"otp:{phone_hash}"
        result = await redis_client.setex(key, 300, otp)  # 5 minutes = 300 seconds
        return result
    except Exception as e:
        logger.error(f"Failed to store OTP: {str(e)}")
        return False

async def verify_otp(phone_hash: str, otp: str) -> bool:
    """
    Verify OTP from Redis
    Returns True if OTP is correct and not expired
    """
    try:
        key = f"otp:{phone_hash}"
        stored_otp = await redis_client.get(key)
        if stored_otp is None:
            return False  # OTP not found or expired
        
        # In a real implementation, we would also check attempt limits here
        # For simplicity, we just compare and delete on success
        if stored_otp == otp:
            # Delete the OTP after successful verification
            await redis_client.delete(key)
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to verify OTP: {str(e)}")
        return False

async def check_otp_rate_limit(phone_hash: str) -> bool:
    """
    Check if OTP request is within rate limits
    Max 3 OTP attempts per 15 minutes
    Returns True if allowed, False if rate limited
    """
    try:
        # Key for tracking attempts
        attempt_key = f"otp_attempts:{phone_hash}"
        # Key for tracking cooldown period
        cooldown_key = f"otp_cooldown:{phone_hash}"
        
        # Check if we're in cooldown period
        cooldown_exists = await redis_client.exists(cooldown_key)
        if cooldown_exists:
            return False
        
        # Get current attempt count
        attempts = await redis_client.get(attempt_key)
        attempts_count = int(attempts) if attempts else 0
        
        if attempts_count >= 3:
            # Set cooldown for 15 minutes
            await redis_client.setex(cooldown_key, 15 * 60, "1")
            return False
        
        # Increment attempt counter
        await redis_client.incr(attempt_key)
        # Set expiry for attempt counter (15 minutes)
        await redis_client.expire(attempt_key, 15 * 60)
        
        return True
    except Exception as e:
        logger.error(f"Failed to check OTP rate limit: {str(e)}")
        # In case of error, allow the request to prevent blocking legitimate users
        return True
