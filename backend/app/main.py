# FILE: ration-saathi/backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import ivr_webhook, cases, analytics, auth, admin
from app.core.config import settings
import logging

# Configure logging
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Ration Saathi API",
    description="IVR-based citizen entitlement and grievance platform for India's PDS",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(ivr_webhook.router, prefix="/ivr", tags=["ivr"])
app.include_router(cases.router, prefix="/cases", tags=["cases"])
app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])

@app.get("/")
async def root():
    return {"message": "Ration Saathi API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
