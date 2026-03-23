# FILE: ration-saathi/backend/app/db/models.py
from sqlalchemy import Column, String, Integer, Boolean, Date, DateTime, Numeric, ForeignKey, CheckConstraint, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()

class RationCard(Base):
    __tablename__ = "ration_cards"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    card_number = Column(String(20), unique=True, nullable=False)
    state_code = Column(String(4), nullable=False)
    district_code = Column(String(6), nullable=False)
    block_code = Column(String(10), nullable=False)
    fps_code = Column(String(12), nullable=False)
    category = Column(String(5), CheckConstraint("category IN ('AAY','PHH','NPHH')"), nullable=False)
    household_head_name = Column(String)  # encrypted
    total_members = Column(Integer, nullable=False)
    phone_hash = Column(String(64))  # HMAC-SHA256
    phone_encrypted = Column(String)  # AES-256-GCM
    is_active = Column(Boolean, default=True)
    aadhaar_seeded = Column(Boolean, default=False)
    last_synced_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

class MonthlyAllocation(Base):
    __tablename__ = "monthly_allocations"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ration_card_id = Column(UUID(as_uuid=True), ForeignKey("ration_cards.id"), nullable=False)
    month_year = Column(Date, nullable=False)  # first day of month
    rice_kg = Column(Numeric(6, 2), default=0)
    wheat_kg = Column(Numeric(6, 2), default=0)
    sugar_kg = Column(Numeric(6, 2), default=0)
    actual_offtake_rice = Column(Numeric(6, 2))  # nullable
    actual_offtake_wheat = Column(Numeric(6, 2))  # nullable
    fps_code = Column(String(12))
    pos_transaction_id = Column(String(50))
    source = Column(String(20), CheckConstraint("source IN ('api_sync','manual','mock')"))
    synced_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (UniqueConstraint('ration_card_id', 'month_year', name='_ration_card_month_uc'),)

class GrievanceCase(Base):
    __tablename__ = "grievance_cases"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_number = Column(String(25), unique=True, nullable=False)  # e.g. RS-RJ-2025-001234
    ration_card_id = Column(UUID(as_uuid=True), ForeignKey("ration_cards.id"))
    reporter_type = Column(String(20), CheckConstraint("reporter_type IN ('self','shg_leader','csc_operator')"))
    reporter_phone_encrypted = Column(String)
    fps_code = Column(String(12), nullable=False)
    district_code = Column(String(6), nullable=False)
    block_code = Column(String(10), nullable=False)
    issue_type = Column(String(30), CheckConstraint("issue_type IN ('short_supply','denial','quality','weighing','other')"))
    reported_month_year = Column(Date, nullable=False)
    expected_wheat_kg = Column(Numeric(6, 2))
    expected_rice_kg = Column(Numeric(6, 2))
    received_wheat_kg = Column(Numeric(6, 2))
    received_rice_kg = Column(Numeric(6, 2))
    voice_testimony_r2_key = Column(String)  # Cloudflare R2 object key
    transcript = Column(String)  # Bhashini STT output
    status = Column(String(25), CheckConstraint("status IN ('open','acknowledged','under_investigation','resolved','closed')"), default='open')
    resolution_notes = Column(String)
    government_ref_number = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class IVRSession(Base):
    __tablename__ = "ivr_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    twilio_call_sid = Column(String(50), unique=True)
    caller_phone_hash = Column(String(64))
    channel = Column(String(30), CheckConstraint("channel IN ('ivr_inbound','missed_call_callback','csc_assisted')"))
    current_state = Column(String(50))
    resolved_card_id = Column(UUID(as_uuid=True), ForeignKey("ration_cards.id"))
    language_selected = Column(String(5), default='hi')
    started_at = Column(DateTime, default=datetime.utcnow)
    last_active_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime)
    call_duration_seconds = Column(Integer)
    is_successful = Column(Boolean, default=False)

class FPSRiskScore(Base):
    __tablename__ = "fps_risk_scores"
    
    fps_code = Column(String(12), primary_key=True)
    district_code = Column(String(6), nullable=False)
    block_code = Column(String(10), nullable=False)
    fps_name = Column(String)
    complaints_30d = Column(Integer, default=0)
    complaints_90d = Column(Integer, default=0)
    resolution_rate = Column(Numeric(5, 2), default=100)
    pos_anomaly_score = Column(Numeric(5, 2), default=0)
    composite_risk_score = Column(Numeric(5, 2), default=0)
    risk_tier = Column(String(10), CheckConstraint("risk_tier IN ('low','medium','high','critical')"), default='low')
    last_calculated_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_hash = Column(String(64), unique=True, nullable=False)
    phone_encrypted = Column(String, nullable=False)
    name = Column(String)
    role = Column(String(30), CheckConstraint("role IN ('csc_operator','shg_leader','block_official','district_admin','state_admin','super_admin')"))
    district_code = Column(String(6))
    block_code = Column(String(10))
    is_active = Column(Boolean, default=True)
    last_login_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
