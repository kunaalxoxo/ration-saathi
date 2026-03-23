import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../backend'))

for k,v in {
    "SUPABASE_URL":"http://localhost:8000","SUPABASE_ANON_KEY":"test","SUPABASE_SERVICE_KEY":"test",
    "DATABASE_URL":"postgresql://postgres:postgres@localhost:5432/test_db",
    "UPSTASH_REDIS_REST_URL":"http://localhost:6379","UPSTASH_REDIS_REST_TOKEN":"test",
    "TWILIO_ACCOUNT_SID":"test","TWILIO_AUTH_TOKEN":"test","TWILIO_PHONE_NUMBER":"+15005550006","TWILIO_WEBHOOK_SECRET":"test",
    "BHASHINI_USER_ID":"test","BHASHINI_API_KEY":"test","BHASHINI_PIPELINE_ID":"test",
    "FAST2SMS_API_KEY":"test","R2_ACCOUNT_ID":"test","R2_ACCESS_KEY_ID":"test",
    "R2_SECRET_ACCESS_KEY":"test","R2_BUCKET_NAME":"test","GROQ_API_KEY":"test",
    "ENCRYPTION_KEY":"bXlFbmNyeXB0aW9uS2V5MTIzNDU2NzgxMjM0NTY3ODEyMzQ=",
    "JWT_SECRET_KEY":"test-jwt-secret-key-that-is-long-enough-for-hs256",
    "ENVIRONMENT":"development","LOG_LEVEL":"DEBUG","USE_MOCK_EPDS":"true","TOLL_FREE_NUMBER":"1800-XXX-XXXX"
}.items():
    os.environ.setdefault(k, v)

import pytest, asyncio
from typing import Generator

@pytest.fixture
def event_loop() -> Generator:
    try: loop = asyncio.get_running_loop()
    except RuntimeError: loop = asyncio.new_event_loop()
    yield loop
    loop.close()
