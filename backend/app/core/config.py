from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"
    SENTRY_DSN: Optional[str] = None

    SUPABASE_URL: str = None  # type: ignore
    SUPABASE_ANON_KEY: str = None  # type: ignore
    SUPABASE_SERVICE_KEY: str = None  # type: ignore
    DATABASE_URL: str = None  # type: ignore

    UPSTASH_REDIS_REST_URL: str = None  # type: ignore
    UPSTASH_REDIS_REST_TOKEN: str = None  # type: ignore

    TWILIO_ACCOUNT_SID: str = None  # type: ignore
    TWILIO_AUTH_TOKEN: str = None  # type: ignore
    TWILIO_PHONE_NUMBER: str = None  # type: ignore
    TWILIO_WEBHOOK_SECRET: str = None  # type: ignore

    BHASHINI_USER_ID: str = None  # type: ignore
    BHASHINI_API_KEY: str = None  # type: ignore
    BHASHINI_PIPELINE_ID: str = None  # type: ignore

    FAST2SMS_API_KEY: str = None  # type: ignore

    R2_ACCOUNT_ID: str = None  # type: ignore
    R2_ACCESS_KEY_ID: str = None  # type: ignore
    R2_SECRET_ACCESS_KEY: str = None  # type: ignore
    R2_BUCKET_NAME: str = None  # type: ignore
    R2_PUBLIC_URL: Optional[str] = None

    GROQ_API_KEY: str = None  # type: ignore

    ENCRYPTION_KEY: str = None  # type: ignore
    JWT_SECRET_KEY: str = None  # type: ignore
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480

    USE_MOCK_EPDS: bool = True
    EPDS_API_BASE_URL: Optional[str] = None
    EPDS_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
