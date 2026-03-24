# FILE: ration-saathi/backend/app/core/redis_client.py
from typing import Optional, Union
import logging

try:
    from upstash_redis import Redis
    UPSTASH_AVAILABLE = True
except ImportError:
    UPSTASH_AVAILABLE = False
    logging.warning("upstash_redis package not installed. Redis functionality will be limited.")

from app.core.config import settings

logger = logging.getLogger(__name__)

class RedisClient:
    def __init__(self):
        if not UPSTASH_AVAILABLE:
            self.redis = None
            logger.warning("Redis client not available due to missing upstash_redis package")
            return
            
        if not settings.UPSTASH_REDIS_REST_URL or not settings.UPSTASH_REDIS_REST_TOKEN:
            self.redis = None
            logger.warning("Upstash Redis credentials not configured")
            return
            
        try:
            self.redis = Redis(
                url=settings.UPSTASH_REDIS_REST_URL,
                token=settings.UPSTASH_REDIS_REST_TOKEN
            )
            logger.info("Upstash Redis client initialized successfully")
        except Exception as e:
            self.redis = None
            logger.error(f"Failed to initialize Upstash Redis client: {str(e)}")

    def get(self, key: str) -> Optional[str]:
        """Get value by key"""
        if not self.redis:
            return None
        try:
            return self.redis.get(key)
        except Exception as e:
            logger.error(f"Error getting key {key} from Redis: {str(e)}")
            return None

    def setex(self, key: str, time: int, value: Union[str, bytes]) -> bool:
        """Set key with expiration time in seconds"""
        if not self.redis:
            return False
        try:
            self.redis.setex(key, time, value)
            return True
        except Exception as e:
            logger.error(f"Error setting key {key} in Redis: {str(e)}")
            return False

    def incr(self, key: str) -> Optional[int]:
        """Increment the integer value of a key by 1"""
        if not self.redis:
            return None
        try:
            return self.redis.incr(key)
        except Exception as e:
            logger.error(f"Error incrementing key {key} in Redis: {str(e)}")
            return None

    def delete(self, *keys: str) -> int:
        """Delete one or more keys"""
        if not self.redis:
            return 0
        try:
            return self.redis.delete(*keys)
        except Exception as e:
            logger.error(f"Error deleting keys {keys} from Redis: {str(e)}")
            return 0

    def exists(self, key: str) -> bool:
        """Check if key exists"""
        if not self.redis:
            return False
        try:
            return bool(self.redis.exists(key))
        except Exception as e:
            logger.error(f"Error checking existence of key {key} in Redis: {str(e)}")
            return False

# Global Redis client instance
redis_client = RedisClient()

# Convenience functions
def get_redis_value(key: str) -> Optional[str]:
    return redis_client.get(key)

def set_redis_value_ex(key: str, time: int, value: Union[str, bytes]) -> bool:
    return redis_client.setex(key, time, value)

def increment_redis_key(key: str) -> Optional[int]:
    return redis_client.incr(key)

def delete_redis_keys(*keys: str) -> int:
    return redis_client.delete(*keys)

def redis_key_exists(key: str) -> bool:
    return redis_client.exists(key)
