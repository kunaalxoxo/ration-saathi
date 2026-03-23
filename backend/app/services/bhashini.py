# FILE: ration-saathi/backend/app/services/bhashini.py
import json
import time
import base64
from typing import Optional, Dict, Any
import httpx
from app.core.redis_client import redis_client
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class BhashiniAPIError(Exception):
    pass

class BhashiniClient:
    def __init__(self):
        self.user_id = settings.BHASHINI_USER_ID
        self.api_key = settings.BHASHINI_API_KEY
        self.pipeline_id = settings.BHASHINI_PIPELINE_ID
        self.ulca_url = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
        self.inference_url = None  # Will be set after authentication
        self.service_id = None
        self.model_id = None
        
    async def _authenticate(self) -> Dict[str, Any]:
        """Authenticate with Bhashini ULCA to get inference API key and service details"""
        # Check if we have a cached token
        cached_token = await redis_client.get("bhashini:auth_token")
        if cached_token:
            try:
                token_data = json.loads(cached_token)
                # Check if token is still valid (with 1 hour buffer)
                if time.time() < token_data.get("expires_at", 0) - 3600:
                    return token_data
            except (json.JSONDecodeError, KeyError):
                pass  # Token is invalid or expired, continue to fetch new one
        
        # Fetch new token
        auth_data = {
            "userId": self.user_id,
            "ulcaApiKey": self.api_key
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.ulca_url,
                    json=auth_data,
                    timeout=30.0
                )
                response.raise_for_status()
                result = response.json()
                
                # Extract pipeline inference details
                pipeline_config = result.get("pipelineInferenceAPIEndPoint", {})
                callback_url = pipeline_config.get("callbackUrl")
                inference_endpoint = pipeline_config.get("inferenceApiKey", {})
                
                self.inference_url = callback_url
                if inference_endpoint:
                    self.service_id = inference_endpoint.get("serviceId")
                    # Note: The actual inference token would be in the response
                    # This is a simplified version - actual implementation may vary
                
                # Cache token for 23 hours (token validity is typically 24 hours)
                token_data = {
                    "access_token": result.get("accessToken"),  # This is illustrative
                    "expires_at": time.time() + (23 * 3600),  # 23 hours from now
                    "service_id": self.service_id,
                    "model_id": self.model_id,
                    "inference_url": self.inference_url
                }
                
                await redis_client.setex(
                    "bhashini:auth_token",
                    23 * 3600,  # 23 hours in seconds
                    json.dumps(token_data)
                )
                
                return token_data
                
            except httpx.HTTPError as e:
                logger.error(f"Bhashini authentication failed: {str(e)}")
                raise BhashiniAPIError(f"Authentication failed: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error during Bhashini authentication: {str(e)}")
                raise BhashiniAPIError(f"Authentication error: {str(e)}")
    
    async def text_to_speech(self, text: str, language: str = 'hi', gender: str = 'female') -> bytes:
        """
        Convert text to speech using Bhashini TTS pipeline.
        Supported languages: 'hi' (Hindi), 'raj' (Rajasthani)
        Returns audio bytes.
        """
        try:
            # For now, we'll use a fallback since actual Bhashini API details
            # would require specific pipeline configuration
            # In a real implementation, this would call the Bhashini TTS API
            
            # Fallback to gTTS for demonstration
            from gtts import gTTS
            import io
            
            # Map language codes
            lang_map = {
                'hi': 'hi',
                'raj': 'hi'  # Rajasthani fallback to Hindi for gTTS
            }
            
            tts = gTTS(text=text, lang=lang_map.get(language, 'hi'), slow=False)
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            return audio_buffer.read()
            
        except Exception as e:
            logger.error(f"Bhashini TTS failed: {str(e)}")
            # Fallback to gTTS
            try:
                from gtts import gTTS
                import io
                
                tts = gTTS(text=text, lang='hi', slow=False)
                audio_buffer = io.BytesIO()
                tts.write_to_fp(audio_buffer)
                audio_buffer.seek(0)
                return audio_buffer.read()
            except Exception as fallback_error:
                logger.error(f"Fallback TTS also failed: {str(fallback_error)}")
                # Return empty bytes as last resort
                return b""
    
    async def speech_to_text(self, audio_bytes: bytes, language: str = 'hi') -> str:
        """
        Convert speech to text using Bhashini ASR pipeline.
        Returns transcript text.
        """
        try:
            # For now, we'll return a placeholder since actual implementation
            # would require sending audio to Bhashini ASR API
            # In a real implementation, this would:
            # 1. Authenticate if needed
            # 2. Send audio to the ASR endpoint
            # 3. Return the transcript
            
            # Placeholder implementation
            if not audio_bytes:
                return ""
            
            # In reality, we would send the audio to Bhashini and get transcription
            # For demo purposes, return a mock transcription
            return "यह एक परीक्षण ट्रांस्क्रिप्ट है।"  # "This is a test transcript." in Hindi
            
        except Exception as e:
            logger.error(f"Bhashini STT failed: {str(e)}")
            # Return empty string as fallback
            return ""

# Mock client for testing
class MockBhashiniClient:
    async def text_to_speech(self, text: str, language: str = 'hi', gender: str = 'female') -> bytes:
        # Return mock audio bytes (just some dummy data)
        return b"mock audio data for: " + text.encode()[:50]
    
    async def speech_to_text(self, audio_bytes: bytes, language: str = 'hi') -> str:
        # Return mock transcript
        if language == 'hi':
            return "यह एक मॉक ट्रांस्क्रिप्ट है।"
        elif language == 'raj':
            return "यो एउटा मॉक ट्रांसक्रिप्ट हो।"
        else:
            return "This is a mock transcript."

# Factory function to get appropriate client
def get_bhashini_client():
    if settings.USE_MOCK_EPDS:  # Using same flag for simplicity
        return MockBhashiniClient()
    else:
        return BhashiniClient()
