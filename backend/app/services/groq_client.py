import httpx
from typing import Dict, Any, Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class GroqClient:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"

    async def _call(self, messages: list) -> Optional[str]:
        if not self.api_key: return None
        async with httpx.AsyncClient() as c:
            try:
                r = await c.post(self.url, headers={"Authorization": f"Bearer {self.api_key}"}, json={"model": self.model, "messages": messages, "max_tokens": 200, "temperature": 0.3}, timeout=30.0)
                r.raise_for_status()
                return r.json()["choices"][0]["message"]["content"].strip()
            except Exception as e:
                logger.error("Groq error: %s", e); return None

    async def generate_scheme_guidance(self, scheme_name: str, language: str = 'hi') -> str:
        prompt = f"Simple Hindi mein 3 sentences mein {scheme_name} ke liye apply karne ka tarika batayein. Aap ka use karein." if language == 'hi' else f"In 3 simple English sentences, explain how to apply for {scheme_name}."
        result = await self._call([{"role":"system","content":"You explain government schemes simply."}, {"role":"user","content":prompt}])
        return result or (f"{scheme_name} ke liye CSC kendra jaayein. Form bharne mein madad milegi. Aadhaar aur ration card le jaayein." if language == 'hi' else f"Visit your nearest CSC center to apply for {scheme_name}.")

    async def generate_resolution_explanation(self, case_details: Dict[str, Any], language: str = 'hi') -> str:
        cn = case_details.get('case_number','Unknown')
        prompt = f"Hindi mein 2 sentences: Case {cn} ki janch ho rahi hai. Nagrik ko kya karna chahiye?" if language == 'hi' else f"2 simple sentences: Case {cn} is under investigation. What should the citizen do?"
        result = await self._call([{"role":"system","content":"You explain complaint resolutions simply."}, {"role":"user","content":prompt}])
        return result or (f"Aapki shikayat {cn} ki janch ki ja rahi hai. SMS se update milega." if language == 'hi' else f"Your complaint {cn} is being investigated. You will receive an SMS update.")


_client = GroqClient()
async def generate_scheme_guidance(name, lang='hi'): return await _client.generate_scheme_guidance(name, lang)
async def generate_resolution_explanation(details, lang='hi'): return await _client.generate_resolution_explanation(details, lang)
