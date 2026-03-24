# Ration Saathi (रशन साथी)

**Ration Saathi** is an AI-powered, IVR-based citizen entitlement and grievance redressal platform designed to empower citizens in India's Public Distribution System (PDS).

## Features
- **Voice-First Interaction:** Citizens can check entitlements and lodge complaints via a simple phone call (IVR).
- **Multilingual Support:** Support for Hindi and regional dialects (e.g., Rajasthani) using Bhashini.
- **Automated Grievance Tracking:** Complaints are automatically logged, transcribed, and assigned.
- **FPS Risk Scoring:** Real-time analytics to identify high-risk Fair Price Shops based on citizen feedback.
- **Admin Dashboard:** Tools for block-level officials to track and resolve cases.

## Tech Stack
- **Backend:** FastAPI, SQLAlchemy, PostgreSQL (Supabase), Redis (Upstash)
- **Frontend:** React, TailwindCSS, Vite
- **IVR/Voice:** Twilio, Bhashini AI, Groq (Whisper/LLM)
- **Infrastructure:** Render (Backend), Vercel (Frontend), Cloudflare R2 (Storage)

---

## Deployment Instructions

### Backend (Render)
1. Fork this repository.
2. Create a new **Web Service** on Render.
3. Connect your repository and select the `backend` directory.
4. Set Environment Variables as defined in `backend/app/core/config.py` (see `.env.example`).
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Worker (Render)
1. Create a new **Worker** service on Render.
2. Use the same repository and `backend` directory.
3. Use the same Environment Variables.
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `celery -A app.worker worker --loglevel=info`

### Frontend (Vercel)
1. Connect your repository to Vercel.
2. Select the `frontend` directory as the root.
3. Set Environment Variable: `VITE_API_URL` to your backend URL (e.g., `https://your-api.onrender.com/api`).
4. Framework Preset: `Vite`.

---

## Local Development & Demo Setup

### 1. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Database Initialization & Seeding
Ensure `DATABASE_URL` and `ENCRYPTION_KEY` are set in your `.env`.
```bash
# From the root directory
python backend/scripts/seed_demo_data.py
```
**Demo Login Credentials:**
- Phone: `9988776655` (OTP is printed in console during dev)
- Role: Block Official

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## License
MIT
