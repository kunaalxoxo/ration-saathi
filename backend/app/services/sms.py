from twilio.rest import Client as TwilioClient
import httpx
import logging
from app.core.config import settings
from upstash_redis import Redis

logger = logging.getLogger(__name__)

class SMSService:
    def __init__(self):
        self.fast2sms_key = settings.FAST2SMS_API_KEY
        self.fast2sms_url = "https://www.fast2sms.com/dev/bulkV2"
        self.twilio_client = None
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
            self.twilio_client = TwilioClient(
                settings.TWILIO_ACCOUNT_SID, 
                settings.TWILIO_AUTH_TOKEN
            )
        self.redis = Redis(
            url=settings.UPSTASH_REDIS_REST_URL,
            token=settings.UPSTASH_REDIS_REST_TOKEN
        )

    async def send_otp_sms(self, phone: str, otp: str) -> bool:
        msg = f"Ration Saathi: Aapka OTP {otp} hai. Yeh 5 minute ke liye vaidh hai."
        logger.info(f"Sending OTP to {phone}")
        return await self._execute_send(phone, msg)

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
        # Try Twilio first if configured
        if self.twilio_client and settings.TWILIO_PHONE_NUMBER:
            try:
                logger.info(f"Attempting to send SMS via Twilio to {phone}")
                self.twilio_client.messages.create(
                    body=msg,
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=f"+91{phone}" if not phone.startswith('+') else phone
                )
                return True
            except Exception as e:
                logger.error(f"Twilio SMS failed: {str(e)}")

        # Fallback to Fast2SMS
        if self.fast2sms_key:
            try:
                logger.info(f"Attempting to send SMS via Fast2SMS to {phone}")
                async with httpx.AsyncClient() as client:
                    resp = await client.post(
                        self.fast2sms_url,
                        data={
                            "route": "q",
                            "message": msg,
                            "language": "english",
                            "numbers": phone
                        },
                        headers={"authorization": self.fast2sms_key}
                    )
                    return resp.status_code == 200
            except Exception as e:
                logger.error(f"Fast2SMS failed: {str(e)}")

        logger.error("No SMS provider configured or all failed")
        return False


sms_service = SMSService()
