# FILE: ration-saathi/backend/app/services/sms.py
from typing import Dict, Optional
import httpx
from app.core.config import settings
from app.core.redis_client import redis_client
import logging

logger = logging.getLogger(__name__)

class Fast2SMSError(Exception):
    pass

class Fast2SMSClient:
    def __init__(self):
        self.api_key = settings.FAST2SMS_API_KEY
        self.sender_id = settings.FAST2SMS_SENDER_ID or "RATION"  # Default sender ID
        self.api_url = "https://www.fast2sms.com/dev/bulkV2"
        
        if not self.api_key:
            logger.warning("FAST2SMS_API_KEY not set - SMS functionality will be limited")

    async def _check_rate_limit(self, phone_hash: str) -> bool:
        """
        Check if we can send SMS to this phone (max 3 per day)
        Returns True if allowed, False if rate limited
        """
        try:
            # Get current count from Redis
            key = f"sms_count:{phone_hash}"
            current_count = await redis_client.get(key)
            
            if current_count is None:
                # First SMS today, set counter with 24 hour expiry
                await redis_client.setex(key, 24 * 3600, 1)
                return True
            
            count = int(current_count)
            if count >= 3:
                return False  # Rate limit exceeded
            
            # Increment counter
            await redis_client.incr(key)
            return True
        except Exception as e:
            logger.error(f"Error checking SMS rate limit: {str(e)}")
            # In case of Redis error, allow the SMS to prevent blocking legitimate requests
            return True

    async def _send_sms(self, phone: str, message: str) -> bool:
        """
        Send SMS via Fast2SMS API
        Returns True if successful, False otherwise
        """
        if not self.api_key:
            logger.error("FAST2SMS_API_KEY not configured")
            return False
            
        headers = {
            "authorization": self.api_key,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "variables_values": message,
            "route": "v3",
            "sender_id": self.sender_id,
            "language": "english",  # Fast2SMS requires this
            "flash": "0",
            "numbers": phone
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    data=data,
                    timeout=30.0
                )
                response.raise_for_status()
                result = response.json()
                
                if result.get("return") == True:
                    logger.info(f"SMS sent successfully to {phone}")
                    return True
                else:
                    logger.error(f"Fast2SMS API returned error: {result}")
                    return False
                    
            except httpx.HTTPError as e:
                logger.error(f"Failed to send SMS via Fast2SMS: {str(e)}")
                return False
            except Exception as e:
                logger.error(f"Unexpected error sending SMS: {str(e)}")
                return False

    async def send_case_created_sms(self, phone: str, case_number: str, language: str = 'hi') -> bool:
        """
        Send SMS when a case is created
        Hindi template: "Ration Saathi: Aapki fariyaad darj hui. Case: {case_number}. Status jaanne ke liye {TOLL_FREE_NUMBER} par call karein."
        """
        # Check rate limit first
        phone_hash = f"hash:{phone}"  # Simple hash for rate limiting - in reality we'd use proper phone hash
        if not await self._check_rate_limit(phone_hash):
            logger.warning(f"Rate limit exceeded for SMS to {phone}")
            return False
        
        # Get appropriate template based on language
        if language == 'hi':
            # In a real app, we'd get this from i18n files
            message = f"Ration Saathi: Aapki fariyaad darj hui. Case: {case_number}. Status jaanne ke liye {settings.TOLL_FREE_NUMBER} par call karein."
        else:
            message = f"Ration Saathi: Your complaint has been registered. Case: {case_number}. For status updates, call {settings.TOLL_FREE_NUMBER}."
        
        return await self._send_sms(phone, message)

    async def send_status_update_sms(self, phone: str, case_number: str, status: str, language: str = 'hi') -> bool:
        """
        Send SMS when case status is updated
        """
        # Check rate limit first
        phone_hash = f"hash:{phone}"  # Simple hash for rate limiting
        if not await self._check_rate_limit(phone_hash):
            logger.warning(f"Rate limit exceeded for SMS to {phone}")
            return False
        
        # Get appropriate template based on language
        if language == 'hi':
            status_map = {
                'open': 'दर्ज',
                'acknowledged': 'स्वीकृत',
                'under_investigation': 'जांच के अधीन',
                'resolved': 'हल',
                'closed': 'बंद'
            }
            status_hindi = status_map.get(status, status)
            message = f"Ration Saathi: Aapke case {case_number} ka status {status_hindi} ho gaya hai. Jaankari ke liye {settings.TOLL_FREE_NUMBER} par call karein."
        else:
            message = f"Ration Saathi: Status of your case {case_number} has been updated to {status}. For more information, call {settings.TOLL_FREE_NUMBER}."
        
        return await self._send_sms(phone, message)

# Global instance
sms_client = Fast2SMSClient()

# Convenience functions
async def send_case_created_sms(phone: str, case_number: str, language: str = 'hi') -> bool:
    return await sms_client.send_case_created_sms(phone, case_number, language)

async def send_status_update_sms(phone: str, case_number: str, status: str, language: str = 'hi') -> bool:
    return await sms_client.send_status_update_sms(phone, case_number, status, language)
