from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    SENTRY_DSN: Optional[str] = None
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str
    DATABASE_URL: str
    UPSTASH_REDIS_REST_URL: str
    UPSTASH_REDIS_REST_TOKEN: str
    TWILIO_ACCOUNT_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_PHONE_NUMBER: str
    TWILIO_WEBHOOK_SECRET: str
    BHASHINI_USER_ID: str
    BHASHINI_API_KEY: str
    BHASHINI_PIPELINE_ID: str
    FAST2SMS_API_KEY: str
    R2_ACCOUNT_ID: str
    R2_ACCESS_KEY_ID: str
    R2_SECRET_ACCESS_KEY: str
    R2_BUCKET_NAME: str
    R2_PUBLIC_URL: Optional[str] = None
    GROQ_API_KEY: str
    ENCRYPTION_KEY: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    USE_MOCK_EPDS: bool = True
    EPDS_API_BASE_URL: Optional[str] = None
    EPDS_API_KEY: Optional[str] = None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
