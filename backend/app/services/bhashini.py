import httpx, json, base64, io
from upstash_redis import Redis
from app.core.config import settings
from gtts import gTTS

class BhashiniClient:
    def __init__(self):
        self.user_id = settings.BHASHINI_USER_ID; self.api_key = settings.BHASHINI_API_KEY
        self.pipeline_id = settings.BHASHINI_PIPELINE_ID
        self.redis = Redis(url=settings.UPSTASH_REDIS_REST_URL, token=settings.UPSTASH_REDIS_REST_TOKEN)
        self.base_url = "https://meity-auth.ulcacontrib.org/ulca/apis/v1"
        self.inference_url = "https://dhruva6.vakyansh.in/services/inference/pipeline"

    async def _get_auth_header(self) -> dict:
        cache_key = "bhashini:auth_token"
        cached = self.redis.get(cache_key)
        if cached: return {"Authorization": cached}
        async with httpx.AsyncClient() as client:
            resp = await client.post(f"{self.base_url}/getUserProfile", headers={"apiKey": self.api_key, "userID": self.user_id})
            if resp.status_code == 200:
                token = resp.json().get("ulcaApiKey")
                self.redis.set(cache_key, token, ex=82800)
                return {"Authorization": token}
            raise Exception("Bhashini Auth Failed")

    async def text_to_speech(self, text: str, language: str = 'hi') -> bytes:
        try:
            auth = await self._get_auth_header()
            payload = {"pipelineTasks": [{"taskType": "tts", "config": {"language": {"sourceLanguage": language}, "serviceId": "ai4bharat/indic-tts--gpu-u4b", "gender": "female"}}], "inputData": {"input": [{"source": text}]}}
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(self.inference_url, json=payload, headers=auth)
                if resp.status_code == 200: return base64.b64decode(resp.json()['pipelineResponse'][0]['audio'][0]['audioContent'])
                raise Exception("Bhashini TTS API Error")
        except:
            tts = gTTS(text=text, lang=language); fp = io.BytesIO(); tts.write_to_fp(fp); return fp.getvalue()

    async def speech_to_text(self, audio: bytes, language: str = 'hi') -> str:
        try:
            auth = await self._get_auth_header(); audio_b64 = base64.b64encode(audio).decode('utf-8')
            payload = {"pipelineTasks": [{"taskType": "asr", "config": {"language": {"sourceLanguage": language}, "serviceId": "ai4bharat/whisper-medium-en-hi--gpu-u4b", "audioFormat": "wav", "samplingRate": 8000}}], "inputData": {"audio": [{"audioContent": audio_b64}]}}
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp = await client.post(self.inference_url, json=payload, headers=auth)
                return resp.json()['pipelineResponse'][0]['output'][0]['source'] if resp.status_code == 200 else ""
        except: return ""

bhashini_client = BhashiniClient()
