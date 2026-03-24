from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from upstash_redis import Redis
from app.core.config import settings
import time

redis = Redis(
    url=settings.UPSTASH_REDIS_REST_URL,
    token=settings.UPSTASH_REDIS_REST_TOKEN
)


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, r: Request, call_next):
        if r.url.path.startswith("/api/ivr/"):
            ip = r.client.host if r.client else "unknown"
            key = f"rate:ivr:{ip}:{int(time.time() / 60)}"
            if redis.incr(key) > 100:
                raise HTTPException(status_code=429)
        return await call_next(r)
