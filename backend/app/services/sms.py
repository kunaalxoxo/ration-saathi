import httpx
from app.core.config import settings
from upstash_redis import Redis


class SMSService:
    def __init__(self):
        self.api_key = settings.FAST2SMS_API_KEY
        self.url = "https://www.fast2sms.com/dev/bulkV2"
        self.redis = Redis(
            url=settings.UPSTASH_REDIS_REST_URL,
            token=settings.UPSTASH_REDIS_REST_TOKEN
        )

    async def send_case_created_sms(self, phone: str, num: str, lang: str = 'hi') -> bool:
        if not await self._check_rate_limit(phone):
            return False
        msg = (
            f"Ration Saathi: Aapki fariyaad darj hui. Case ID: {num}. "
            f"Status jaanne ke liye {settings.TWILIO_PHONE_NUMBER} par call karein."
        )
        return await self._execute_send(phone, msg)

    async def _check_rate_limit(self, phone: str) -> bool:
        from app.core.encryption import encryption_service
        key = f"limit:sms:{encryption_service.hash_for_lookup(phone)}"
        count = self.redis.incr(key)
        if count == 1:
            self.redis.expire(key, 86400)
        return count <= 3

    async def _execute_send(self, phone: str, msg: str) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    self.url,
                    data={
                        "route": "q",
                        "message": msg,
                        "language": "english",
                        "numbers": phone
                    },
                    headers={"authorization": self.api_key}
                )
                return resp.status_code == 200
        except Exception:
            return False


sms_service = SMSService()
