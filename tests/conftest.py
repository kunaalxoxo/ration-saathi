import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../backend'))

# Set environment variables for testing
os.environ["SUPABASE_URL"] = "http://localhost:8000"
os.environ["SUPABASE_ANON_KEY"] = "test-anon-key"
os.environ["SUPABASE_SERVICE_KEY"] = "test-service-key"
os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5432/postgres"
os.environ["UPSTASH_REDIS_REST_URL"] = "localhost:6379"
os.environ["UPSTASH_REDIS_REST_TOKEN"] = "test-token"
os.environ["TWILIO_ACCOUNT_SID"] = "test-sid"
os.environ["TWILIO_AUTH_TOKEN"] = "test-token"
os.environ["TWILIO_PHONE_NUMBER"] = "+15005550006"
os.environ["TWILIO_WEBHOOK_SECRET"] = "test-secret"
os.environ["BHASHINI_USER_ID"] = "test-user"
os.environ["BHASHINI_API_KEY"] = "test-key"
os.environ["BHASHINI_PIPELINE_ID"] = "test-pipeline"
os.environ["FAST2SMS_API_KEY"] = "test-key"
os.environ["R2_ACCOUNT_ID"] = "test-account-id"
os.environ["R2_ACCESS_KEY_ID"] = "test-access-key-id"
os.environ["R2_SECRET_ACCESS_KEY"] = "test-secret-access-key"
os.environ["R2_BUCKET_NAME"] = "test-bucket"
os.environ["GROQ_API_KEY"] = "test-key"
os.environ["ENCRYPTION_KEY"] = "bXlFbmNyeXB0aW9uS2V5MTIzNDU2NzgxMjM0NTY3ODEyMzQ="
os.environ["JWT_SECRET_KEY"] = "test-jwt-secret-key-that-is-long-enough-for-hs256"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "480"
os.environ["ENVIRONMENT"] = "development"
os.environ["LOG_LEVEL"] = "DEBUG"
os.environ["SENTRY_DSN"] = ""
os.environ["USE_MOCK_EPDS"] = "true"
os.environ["EPDS_API_BASE_URL"] = ""
os.environ["EPDS_API_KEY"] = ""
os.environ["TOLL_FREE_NUMBER"] = "1800-XXX-XXXX"

import pytest
import asyncio
from typing import Generator, AsyncGenerator
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client() -> Generator:
    with TestClient(app) as c:
        yield c

@pytest.fixture
def event_loop() -> Generator:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()
