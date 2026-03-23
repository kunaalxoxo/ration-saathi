# RATION SAATHI ARCHITECTURE

## ASCII Architecture Diagram

[Feature Phone] ──call──► [Twilio IVR] ──webhook──► [FastAPI on Render]
                                                            │
                               ┌────────────────────────────┤
                               ▼                            ▼
                    [Supabase PostgreSQL]         [Upstash Redis]
                    (ration cards, cases,         (IVR session state,
                     analytics, users)             call context, OTP)
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
             [Bhashini API]        [Groq API]
             (Hindi STT/TTS)       (guidance text, free LLM)
                    │
                    ▼
             [Fast2SMS]
             (case ID + status SMS)
                    │
                    ▼
             [Cloudflare R2]
             (voice testimony audio files)

[CSC/SHG Operator] ──► [React PWA on Vercel] ──► [FastAPI on Render]
[District Official] ──► [Admin Dashboard]    ──► [Analytics API]
                                                  [DuckDB embedded]

## Technology Justification

(a) Why Supabase over a self-hosted PostgreSQL:
Supabase provides a free managed PostgreSQL database with built-in authentication helpers, real-time subscriptions, and automatic backups. This eliminates the operational overhead of managing database servers, patches, and scaling while staying within free tier limits (500MB storage). The built-in REST API also simplifies frontend integration.

(b) Why Upstash over standard Redis:
Upstash Redis offers a serverless, HTTP-based Redis client that works perfectly on Render's free tier where persistent TCP connections are often restricted or unavailable. With 10,000 commands/day free tier, it's sufficient for IVR session storage and OTP verification without requiring complex connection management.

(c) Why Bhashini over Google STT:
Bhashini is completely free, government-backed, and supports 22 Indian languages including Rajasthani dialects. Unlike commercial APIs that charge per character, Bhashini has no billing ever, making it ideal for a social impact project. It also aligns with India's digital sovereignty goals.

(d) Why Groq free tier over OpenAI:
Groq offers generous free rate limits with the fastest inference speeds available. The Llama 3.3 70B model is more than sufficient for generating short guidance text in Hindi/English. This avoids the cost and complexity of proprietary LLMs while maintaining high-quality output.

(e) Why Cloudflare R2 over S3:
Cloudflare R2 provides an S3-compatible API so code changes are minimal when migrating, but with zero egress fees and 10GB free storage forever. This is crucial for storing voice testimonies where egress costs on S3 could quickly exceed budgets at scale.

(f) Why Render over Railway/Heroku:
Render offers the most generous free tier for Python web services in 2025 with no credit card required for basic tier. It provides automatic HTTPS, custom domains, and continuous deployment from GitHub - all essential for a hackathon project that needs to be demo-ready without financial barriers.
