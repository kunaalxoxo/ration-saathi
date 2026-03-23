# Ration Saathi

A voice-first, IVR-based citizen entitlement and grievance platform for India's Public Distribution System (PDS). Built for KRITI Social Impact Challenge, BITS Pilani Apogee 2026.

## Features

- **IVR Interface**: Call from any feature phone to check entitlements and lodge complaints
- **Multi-language Support**: Hindi and Rajasthani language support via Bhashini API
- **Grievance Management**: Structured complaint logging with case ID generation
- **SMS Notifications**: Case ID and status updates via Fast2SMS
- **Analytics Dashboard**: FPS risk scoring and complaint trends for officials
- **Offline-First PWA**: React frontend with offline capabilities
- **Zero-Cost Infrastructure**: Built entirely on free tier services

## Architecture

![Architecture Diagram](ARCHITECTURE.md)

### Technology Stack

- **Backend**: Python 3.12 + FastAPI (async, perfect for concurrent IVR webhook calls)
- **Database**: Supabase PostgreSQL (free managed DB, built-in REST API as bonus)
- **Cache**: Upstash Redis (serverless, HTTP-based Redis client works on Render free tier)
- **IVR**: Twilio (primary, free trial credits) + Asterisk AGI (self-hosted fallback, document setup)
- **Voice AI**: Bhashini API (free govt API for Hindi STT/TTS, no cost ever)
- **SMS**: Fast2SMS (free credits, DLT-compliant India SMS)
- **Storage**: Cloudflare R2 (voice testimonies, free 10GB)
- **Frontend**: React 18 + Vite + Tailwind CSS, hosted on Vercel free tier
- **Maps**: Leaflet.js + OpenStreetMap tiles (zero cost)
- **LLM**: Groq API free tier (Llama 3.3 70B for guidance text generation)
- **Analytics**: Plain PostgreSQL + DuckDB (embedded, no separate service needed)

## Quick Start

### Prerequisites

- Git
- Docker and Docker Compose
- Accounts for the following services (all free tiers):
  - [Supabase](https://supabase.com)
  - [Upstash Redis](https://upstash.com)
  - [Twilio](https://twilio.com)
  - [Bhashini](https://bhashini.gov.in)
  - [Fast2SMS](https://www.fast2sms.com)
  - [Cloudflare](https://cloudflare.com) (for R2)
  - [Groq](https://groq.com)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ration-saathi.git
   cd ration-saathi
   ```

2. Copy the example environment file and fill in your credentials:
   ```bash
   cp .env.example .env
   # Edit .env with your actual credentials from the service providers
   ```

3. Start the application with Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. The application will be available at:
   - Backend API: http://localhost:8000
   - Frontend: http://localhost:3000
   - API Documentation: http://localhost:8000/docs

### Environment Variables

See `.env.example` for all required environment variables with detailed comments.

## Running the Demo

Follow these steps to demonstrate Ration Saathi to judges or stakeholders:

### Step 1: Show the CSC Dashboard
1. Open the frontend at http://localhost:3000
2. Login as a CSC operator (use demo credentials: phone 9999999999, OTP 123456)
3. Navigate to the Home dashboard to see:
   - Cases filed today
   - Pending cases
   - Quick statistics

### Step 2: Check Entitlement Details
1. From the Home dashboard, click "Check Entitlement"
2. Enter a demo ration card number (e.g., `RJ-BA-2025-00001`)
3. Verify the entitlement details appear instantly:
   - Card holder name
   - Family members
   - This month's wheat and rice allocation
4. Click "Less Received? Lodge Complaint" to proceed to complaint filing

### Step 3: Lodge a Complaint
1. Confirm the ration card details
2. Select issue type (e.g., "Short Supply" for wheat)
3. Enter received quantity (e.g., 3.0 kg when expected was 5.0 kg)
4. Select the FPS from the dropdown
5. Optionally: Take a photo of the weighing slip
6. Click "Submit" to lodge the complaint
7. Verify:
   - Case number appears in large green text
   - Success message with instructions to keep the case number safe
   - Copy button to copy the case number
   - Automatic SMS trigger (in demo mode, shows what SMS would be sent)

### Step 4: View Admin Dashboard
1. Logout and login as an admin (use demo credentials: phone 8888888888, OTP 654321)
2. Navigate to the Admin Dashboard
3. View:
   - Overview cards with total/open/resolved cases
   - FPS Risk Table showing the demo FPS now with updated risk score
   - District Heatmap showing complaint locations
   - Complaint Trends chart showing monthly trends

### Step 5: Test the IVR System
1. Call the Twilio number configured in your `.env` file
2. Experience the IVR flow in Hindi:
   - Language selection (press 1 for Hindi, 2 for Rajasthani)
   - Enter ration card number followed by *
   - Hear entitlement announcement (personalized with name)
   - Confirm if full allocation was received
   - If less received, select complaint type
   - Enter received quantity followed by *
   - Receive case number and SMS confirmation
3. Alternatively, use the missed-call flow:
   - Call the number and hang up before answered
   - Receive a callback within 2 minutes
   - Go through the same IVR flow

### Step 6: Verify Data Persistence
1. Check that the complaint appears in:
   - CSC dashboard under pending cases
   - Admin dashboard FPS risk table
   - Case tracker when entering the case number
2. Verify that risk scores updated appropriately

## Project Structure

```
ration-saathi/
├── backend/                    # Python/FastAPI backend
│   ├── app/
│   │   ├── api/               # API routers (IVR, cases, analytics, auth, admin)
│   │   ├── core/              # Configuration, security, logging, encryption
│   │   ├── db/                # Database models and session
│   │   ├── ivr/               # IVR flow engine and state machine
│   │   ├── services/          # Business logic (entitlement, grievance, analytics, etc.)
│   │   └── utils/             # Helper functions
│   ├── tests/                 # Unit and integration tests
│   ├── mock_data/             # Mock e-PDS fixtures for hackathon demo
│   ├── Dockerfile             # Containerization
│   ├── render.yaml            # Render.com deployment config
│   └── requirements.txt       # Python dependencies
├── frontend/                  # React/Vite frontend
│   ├── src/
│   │   ├── pages/             # Login, Home, EntitlementCheck, LodgeComplaint, etc.
│   │   ├── components/        # Reusable UI components
│   │   ├── i18n/              # Internationalization (hi.json, en.json)
│   │   └── lib/               # API client, auth context, offline queue
│   ├── public/
│   ├── vercel.json            # Vercel deployment config
│   └── package.json           # Node.js dependencies
├── ivr-scripts/               # IVR scripts for Twilio and Asterisk
│   ├── twilio/                # TwiML XML responses
│   └── asterisk/              # Asterisk AGI scripts for self-hosted fallback
├── .github/
│   └── workflows/             # CI/CD pipelines (GitHub Actions)
│       ├── ci.yml             # Continuous Integration
│       └── deploy.yml         # Continuous Deployment
├── ARCHITECTURE.md            # Detailed architecture and technology justification
├── database_schema.sql        # Complete SQL schema for Supabase
└── README.md                  # This file
```

## Deployment

### Backend (Render.com)

1. Create a new Web Service on Render.com
2. Connect your GitHub repository
3. Set the build command to: `pip install -r requirements.txt`
4. Set the start command to: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add all environment variables from `.env` as service secrets
6. Enable auto-deploy from GitHub pushes

### Frontend (Vercel)

1. Import the project to Vercel
2. Vercel will automatically detect the Vite project
3. Add environment variables from `.env` as project environment variables
4. Enable auto-deploy from GitHub pushes

### IVR Number Configuration

1. Purchase a Twilio number (or use your free trial credit)
2. Configure the number's webhook to point to:
   - `https://your-render-service.onrender.com/ivr/inbound` (for incoming calls)
   - `https://your-render-service.onrender.com/ivr/missed-call` (for missed calls)
3. Set up your Twilio Auth
