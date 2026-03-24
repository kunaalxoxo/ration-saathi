-- Enable UUID and Crypto extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- Table: ration_cards
CREATE TABLE ration_cards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    card_number VARCHAR(20) UNIQUE NOT NULL,
    state_code VARCHAR(4) NOT NULL,
    district_code VARCHAR(6) NOT NULL,
    block_code VARCHAR(10) NOT NULL,
    fps_code VARCHAR(12) NOT NULL,
    category VARCHAR(5) CHECK (category IN ('AAY','PHH','NPHH')),
    household_head_name TEXT,
    total_members SMALLINT NOT NULL,
    phone_hash VARCHAR(64),
    phone_encrypted TEXT,
    is_active BOOLEAN DEFAULT true,
    aadhaar_seeded BOOLEAN DEFAULT false,
    last_synced_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table: monthly_allocations
CREATE TABLE monthly_allocations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    ration_card_id UUID REFERENCES ration_cards(id),
    month_year DATE NOT NULL,
    rice_kg NUMERIC(6,2) DEFAULT 0,
    wheat_kg NUMERIC(6,2) DEFAULT 0,
    sugar_kg NUMERIC(6,2) DEFAULT 0,
    actual_offtake_rice NUMERIC(6,2),
    actual_offtake_wheat NUMERIC(6,2),
    fps_code VARCHAR(12),
    pos_transaction_id VARCHAR(50),
    source VARCHAR(20) CHECK (source IN ('api_sync','manual','mock')),
    synced_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(ration_card_id, month_year)
);

-- Table: grievance_cases
CREATE TABLE grievance_cases (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    case_number VARCHAR(25) UNIQUE NOT NULL,
    ration_card_id UUID REFERENCES ration_cards(id),
    reporter_type VARCHAR(20) CHECK (reporter_type IN ('self','shg_leader','csc_operator')),
    reporter_phone_encrypted TEXT,
    fps_code VARCHAR(12) NOT NULL,
    district_code VARCHAR(6) NOT NULL,
    block_code VARCHAR(10) NOT NULL,
    issue_type VARCHAR(30) CHECK (issue_type IN ('short_supply','denial','quality','weighing','other')),
    reported_month_year DATE NOT NULL,
    expected_wheat_kg NUMERIC(6,2),
    expected_rice_kg NUMERIC(6,2),
    received_wheat_kg NUMERIC(6,2),
    received_rice_kg NUMERIC(6,2),
    voice_testimony_r2_key TEXT,
    transcript TEXT,
    status VARCHAR(25) DEFAULT 'open' CHECK (status IN ('open','acknowledged','under_investigation','resolved','closed')),
    resolution_notes TEXT,
    government_ref_number VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table: ivr_sessions
CREATE TABLE ivr_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    twilio_call_sid VARCHAR(50) UNIQUE,
    caller_phone_hash VARCHAR(64),
    channel VARCHAR(30) CHECK (channel IN ('ivr_inbound','missed_call_callback','csc_assisted')),
    current_state VARCHAR(50),
    resolved_card_id UUID REFERENCES ration_cards(id),
    language_selected VARCHAR(5) DEFAULT 'hi',
    started_at TIMESTAMPTZ DEFAULT NOW(),
    last_active_at TIMESTAMPTZ DEFAULT NOW(),
    ended_at TIMESTAMPTZ,
    call_duration_seconds INTEGER,
    is_successful BOOLEAN DEFAULT false
);

-- Table: fps_risk_scores
CREATE TABLE fps_risk_scores (
    fps_code VARCHAR(12) PRIMARY KEY,
    district_code VARCHAR(6) NOT NULL,
    block_code VARCHAR(10) NOT NULL,
    fps_name TEXT,
    complaints_30d INTEGER DEFAULT 0,
    complaints_90d INTEGER DEFAULT 0,
    resolution_rate NUMERIC(5,2) DEFAULT 100,
    pos_anomaly_score NUMERIC(5,2) DEFAULT 0,
    composite_risk_score NUMERIC(5,2) DEFAULT 0,
    risk_tier VARCHAR(10) DEFAULT 'low' CHECK (risk_tier IN ('low','medium','high','critical')),
    last_calculated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Table: users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone_hash VARCHAR(64) UNIQUE NOT NULL,
    phone_encrypted TEXT NOT NULL,
    name TEXT,
    role VARCHAR(30) CHECK (role IN ('csc_operator','shg_leader','block_official','district_admin','state_admin','super_admin')),
    district_code VARCHAR(6),
    block_code VARCHAR(10),
    is_active BOOLEAN DEFAULT true,
    last_login_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_ration_cards_fps ON ration_cards(fps_code);
CREATE INDEX idx_ration_cards_district ON ration_cards(district_code);
CREATE INDEX idx_ration_cards_phone_hash ON ration_cards(phone_hash);
CREATE INDEX idx_grievances_fps_status ON grievance_cases(fps_code, status);
CREATE INDEX idx_grievances_district ON grievance_cases(district_code, created_at DESC);
CREATE INDEX idx_grievances_card ON grievance_cases(ration_card_id, created_at DESC);
CREATE INDEX idx_allocations_card_month ON monthly_allocations(ration_card_id, month_year DESC);
