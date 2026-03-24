import httpx
from app.core.config import settings


class GroqClient:
    def __init__(self):
        self.api_key = settings.GROQ_API_KEY
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.3-70b-versatile"

    async def generate_scheme_guidance(self, scheme: str, lang: str = 'hi') -> str:
        p = f"In simple {lang} (Class 5 level), explain in 3 short sentences how to apply for {scheme}. Be warm (aap). Under 50 words."
        return await self._call_groq(p)

    async def generate_resolution_explanation(self, details: dict, lang: str = 'hi') -> str:
        p = f"Explain resolution in simple {lang}: {details.get('notes')}. Helpfull/official. Max 2 sentences."
        return await self._call_groq(p)

    async def _call_groq(self, p: str) -> str:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    self.url,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "model": self.model,
                        "messages": [{"role": "user", "content": p}],
                        "max_tokens": 200,
                        "temperature": 0.5
                    },
                    timeout=5.0
                )
                if resp.status_code == 200:
                    return resp.json()['choices'][0]['message']['content'].strip()
                return "Kripya intezar karein."
        except Exception:
            return "Kripya apne nazdiki CSC kendra se sampark karein."


groq_client = GroqClient()
