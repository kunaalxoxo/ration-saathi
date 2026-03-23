# FILE: ration-saathi/backend/app/services/groq_client.py
import json
from typing import Optional, Dict, Any
import httpx
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

class GroqAPIError(Exception):
    pass

class GroqClient:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"
        self.max_tokens = 200
        self.temperature = 0.3
        
        if not self.api_key:
            logger.warning("GROQ_API_KEY not set - Groq client will not function")

    async def _make_request(self, messages: list) -> Optional[str]:
        """Make request to Groq API"""
        if not self.api_key:
            raise GroqAPIError("GROQ_API_KEY not configured")
            
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                result = response.json()
                
                # Extract the generated text
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"].strip()
                else:
                    logger.error(f"Unexpected Groq API response format: {result}")
                    return None
                    
            except httpx.HTTPError as e:
                logger.error(f"Groq API request failed: {str(e)}")
                raise GroqAPIError(f"API request failed: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error during Groq API request: {str(e)}")
                raise GroqAPIError(f"API error: {str(e)}")

    async def generate_scheme_guidance(self, scheme_name: str, user_language: str = 'hi') -> str:
        """
        Generate guidance text for a government scheme in simple language.
        Prompt: "In simple Hindi (Class 5 level), explain in 3 sentences how to apply for {scheme_name}. Be warm and use respectful language (aap). No jargon."
        """
        # Language mapping for prompt
        lang_instruction = {
            'hi': "In simple Hindi (Class 5 level), explain in 3 sentences how to apply for {scheme_name}. Be warm and use respectful language (aap). No jargon.",
            'en': "In simple English (Grade 5 level), explain in 3 sentences how to apply for {scheme_name}. Be warm and use respectful language. No jargon."
        }
        
        instruction = lang_instruction.get(user_language, lang_instruction['hi'])
        prompt = instruction.format(scheme_name=scheme_name)
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant that explains government schemes in simple, respectful language."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            result = await self._make_request(messages)
            if result:
                return result
            else:
                # Fallback to hardcoded template
                return self._get_fallback_scheme_guidance(scheme_name, user_language)
        except Exception as e:
            logger.error(f"Failed to generate scheme guidance: {str(e)}")
            return self._get_fallback_scheme_guidance(scheme_name, user_language)

    async def generate_resolution_explanation(self, case_details: Dict[str, Any], language: str = 'hi') -> str:
        """
        Generate explanation of case resolution in plain language for IVR playback.
        """
        # Create prompt based on case details
        if language == 'hi':
            prompt = f"""एक सरल हिंदी में (कक्षा 5 स्तर), इस शिकायत का समाधान समझाएं: 
            राशन कार्ड संख्या: {case_details.get('ration_card_number', 'अज्ञात')}
            महीना: {case_details.get('reported_month_year', 'अज्ञात')}
            शिकायत का प्रकार: {case_details.get('issue_type', 'अज्ञात')}
            अपेक्षित गेहूं: {case_details.get('expected_wheat_kg', 0)} किग्रा
            प्राप्त गेहूं: {case_details.get('received_wheat_kg', 0)} किग्रा
            अपेक्षित चावल: {case_details.get('expected_rice_kg', 0)} किग्रा
            प्राप्त चावल: {case_details.get('received_rice_kg', 0)} किग्रा
            कृपया 3 वाक्यों में स्पष्ट करें कि क्या कार्रवाई की गई है और नागरिक को क्या करना चाहिए। सम्मानजनक भाषा (आप) का उपयोग करें।"""
        else:
            prompt = f"""In simple English (Grade 5 level), explain the resolution of this complaint:
            Ration card number: {case_details.get('ration_card_number', 'Unknown')}
            Month: {case_details.get('reported_month_year', 'Unknown')}
            Issue type: {case_details.get('issue_type', 'Unknown')}
            Expected wheat: {case_details.get('expected_wheat_kg', 0)} kg
            Received wheat: {case_details.get('received_wheat_kg', 0)} kg
            Expected rice: {case_details.get('expected_rice_kg', 0)} kg
            Received rice: {case_details.get('received_rice_kg', 0)} kg
            Please explain in 3 sentences what action has been taken and what the citizen should do. Use respectful language."""
        
        messages = [
            {"role": "system", "content": "You are a helpful assistant that explains complaint resolutions in simple, respectful language."},
            {"role": "user", "content": prompt}
        ]
        
        try:
            result = await self._make_request(messages)
            if result:
                return result
            else:
                # Fallback to hardcoded template
                return self._get_fallback_resolution_explanation(case_details, language)
        except Exception as e:
            logger.error(f"Failed to generate resolution explanation: {str(e)}")
            return self._get_fallback_resolution_explanation(case_details, language)

    def _get_fallback_scheme_guidance(self, scheme_name: str, language: str = 'hi') -> str:
        """Fallback guidance text when Groq API is unavailable"""
        if language == 'hi':
            return f"{scheme_name} के लिए आवेदन करने के लिए, अपने नजदीकी CSC केंद्र पर जाएं। वहां आपको आवेदन फॉर्म भरने में मदद मिलेगी। सभी आवश्यक दस्तावेज जैसे आधार कार्ड, राशन कार्ड और बैंक पासबुक साथ लाएं।"
        else:
            return f"To apply for {scheme_name}, visit your nearest CSC center. They will help you fill out the application form. Bring all necessary documents like Aadhaar card, ration card, and bank passbook."

    def _get_fallback_resolution_explanation(self, case_details: Dict[str, Any], language: str = 'hi') -> str:
        """Fallback resolution explanation when Groq API is unavailable"""
        if language == 'hi':
            return f"आपकी शिकायत दर्ज कर ली गई है और जांच के लिए भेज दी गई है। आप अपने केस नंबर {case_details.get('case_number', 'अज्ञात')} पर स्थिति की जांच कर सकते हैं। जांच पूरी होने पर आपको SMS के माध्यम से सूचित कर दिया जाएगा।"
        else:
            return f"Your complaint has been registered and forwarded for investigation. You can check the status using your case number {case_details.get('case_number', 'Unknown')}. You will be notified via SMS once the investigation is complete."

# Global instance
groq_client = GroqClient()

# Convenience functions
async def generate_scheme_guidance(scheme_name: str, user_language: str = 'hi') -> str:
    return await groq_client.generate_scheme_guidance(scheme_name, user_language)

async def generate_resolution_explanation(case_details: Dict[str, Any], language: str = 'hi') -> str:
    return await groq_client.generate_res
