import httpx
import logging
from app.core.config import settings
from upstash_redis import Redis

logger = logging.getLogger(__name__)

class SMSService:
    def __init__(self):
        self.fast2sms_key = settings.FAST2SMS_API_KEY
        self.fast2sms_url = "https://www.fast2sms.com/dev/bulkV2"
        self.redis = Redis(
            url=settings.UPSTASH_REDIS_REST_URL,
            token=settings.UPSTASH_REDIS_REST_TOKEN
        )

    async def send_otp_sms(self, phone: str, otp: str) -> bool:
        msg = f"Ration Saathi: Aapka OTP {otp} hai. Yeh 5 minute ke liye vaidh hai."
        logger.info(f"Preparing OTP SMS for {phone}")
        return await self._execute_send(phone, msg)

    async def send_case_created_sms(self, phone: str, num: str, lang: str = 'hi') -> bool:
        if not await self._check_rate_limit(phone):
            return False
        msg = (
            f"Ration Saathi: Aapki fariyaad darj hui. Case ID: {num}. "
            f"Status jaanne ke liye humein call karein."
        )
        return await self._execute_send(phone, msg)

    async def _check_rate_limit(self, phone: str) -> bool:
        from app.core.encryption import encryption_service
        key = f"limit:sms:{encryption_service.hash_for_lookup(phone)}"
        count = self.redis.incr(key)
        if count == 1:
            self.redis.expire(key, 86400)
        return count <= 10  # Increased limit for testing

    async def _execute_send(self, phone: str, msg: str) -> bool:
        if not self.fast2sms_key:
            logger.error("FAST2SMS_API_KEY not configured")
            return False

        # Fast2SMS requires numbers without +91
        clean_phone = phone.replace("+91", "").strip()
        
        try:
            logger.info(f"Sending SMS via Fast2SMS to {clean_phone}")
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    self.fast2sms_url,
                    data={
                        "route": "q",
                        "message": msg,
                        "language": "english",
                        "numbers": clean_phone
                    },
                    headers={"authorization": self.fast2sms_key}
                )
                
                resp_json = resp.json()
                logger.info(f"Fast2SMS Response for {clean_phone}: {resp_json}")
                
                if resp.status_code == 200 and resp_json.get("return") is True:
                    return True
                else:
                    logger.error(f"Fast2SMS delivery failed: {resp_json.get('message')}")
                    return False
        except Exception as e:
            logger.error(f"Fast2SMS request failed: {str(e)}")
            return False


sms_service = SMSService()
