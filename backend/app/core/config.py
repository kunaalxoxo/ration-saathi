# FILE: ration-saathi/backend/app/core/config.py
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # ── SUPABASE ──────────────────────────────────
    SUPABASE_URL: str = Field(..., description="From Supabase project Settings > API > Project URL")
    SUPABASE_ANON_KEY: str = Field(..., description="From Supabase Settings > API > anon public key")
    SUPABASE_SERVICE_KEY: str = Field(..., description="From Supabase Settings > API > service_role key (backend only)")
    DATABASE_URL: str = Field(..., description="postgresql://postgres:[password]@db.[ref].supabase.co:5432/postgres")

    # ── UPSTASH REDIS ─────────────────────────────
    UPSTASH_REDIS_REST_URL: str = Field(..., description="From Upstash console > your DB > REST URL")
    UPSTASH_REDIS_REST_TOKEN: str = Field(..., description="From Upstash console > your DB > REST Token")

    # ── TWILIO ────────────────────────────────────
    TWILIO_ACCOUNT_SID: str = Field(..., description="From Twilio console > Account Info")
    TWILIO_AUTH_TOKEN: str = Field(..., description="From Twilio console > Account Info")
    TWILIO_PHONE_NUMBER: str = Field(..., description="Your Twilio number (e.g. +918XXXXXXXXX)")
    TWILIO_WEBHOOK_SECRET: str = Field(..., description="Random string you set; used to verify Twilio requests")

    # ── BHASHINI API ──────────────────────────────
    BHASHINI_USER_ID: str = Field(..., description="From bhashini.gov.in after registration")
    BHASHINI_API_KEY: str = Field(..., description="From Bhashini ULCA dashboard")
    BHASHINI_PIPELINE_ID: str = Field(..., description="Pipeline ID for Hindi ASR+TTS from Bhashini")

    # ── FAST2SMS ──────────────────────────────────
    FAST2SMS_API_KEY: str = Field(..., description="From fast2sms.com dashboard > Dev API")
    FAST2SMS_SENDER_ID: Optional[str] = Field(default="RATION", description="DLT registered sender ID")

    # ── CLOUDFLARE R2 ─────────────────────────────
    R2_ACCOUNT_ID: str = Field(..., description="From Cloudflare dashboard > R2")
    R2_ACCESS_KEY_ID: str = Field(..., description="R2 API token Access Key ID")
    R2_SECRET_ACCESS_KEY: str = Field(..., description="R2 API token Secret Access Key")
    R2_BUCKET_NAME: str = Field(..., description="Your R2 bucket name (e.g. ration-saathi-audio)")
    R2_PUBLIC_URL: Optional[str] = Field(default=None, description="Public URL if bucket is public (optional)")

    # ── GROQ ──────────────────────────────────────
    GROQ_API_KEY: str = Field(..., description="From console.groq.com > API Keys (free)")

    # ── APP SECURITY ──────────────────────────────
    ENCRYPTION_KEY: str = Field(..., description="32-byte base64 key: python -c \"import secrets,base64; print(base64.b64encode(secrets.token_bytes(32)).decode())\"")
    JWT_SECRET_KEY: str = Field(..., description="Random 64-char string")
    JWT_ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=480)

    # ── APP CONFIG ────────────────────────────────
    ENVIRONMENT: str = Field(default="development", description="development | staging | production")
    LOG_LEVEL: str = Field(default="INFO")
    SENTRY_DSN: Optional[str] = Field(default=None, description="From sentry.io > your project > DSN (leave blank in dev)")

    # ── MOCK e-PDS (for hackathon demo) ───────────
    USE_MOCK_EPDS: bool = Field(default=True, description="Set to true to use mock_data/ fixtures instead of real API")
    EPDS_API_BASE_URL: Optional[str] = Field(default=None, description="Real state e-PDS API base URL (if available)")
    EPDS_API_KEY: Optional[str] = Field(default=None, description="Real e-PDS API key (if available)")
    
    # ── OTHER SETTINGS ────────────────────────────
    TOLL_FREE_NUMBER: str = Field(default="1800-XXX-XXXX", description="Toll-free number for status inquiries")
    
    @field_validator('ENVIRONMENT')
    @classmethod
    def validate_environment(cls, v):
        allowed = ['development', 'staging', 'production']
        if v not in allowed:
            raise ValueError(f'ENVIRONMENT must be one of {allowed}')
        return v
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True,
        "extra": "ignore"
    }

# Global settings instance
settings = Settings()
