from datetime import date, datetime
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func
import uuid

Base = declarative_base()

class RationCard(Base):
    __tablename__ = "ration_cards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    card_number = Column(String(20), unique=True, nullable=False, index=True)
    state_code = Column(String(4), nullable=False)
    district_code = Column(String(6), nullable=False, index=True)
    block_code = Column(String(10), nullable=False)
    fps_code = Column(String(12), nullable=False, index=True)
    category = Column(String(5))
    household_head_name = Column(Text)  # Encrypted in DB
    total_members = Column(Integer, nullable=False)
    phone_hash = Column(String(64), index=True)
    phone_encrypted = Column(Text)
    is_active = Column(Boolean, default=True)
    aadhaar_seeded = Column(Boolean, default=False)
    last_synced_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    allocations = relationship("MonthlyAllocation", back_populates="ration_card")
    grievances = relationship("GrievanceCase", back_populates="ration_card")

class MonthlyAllocation(Base):
    __tablename__ = "monthly_allocations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ration_card_id = Column(UUID(as_uuid=True), ForeignKey("ration_cards.id"))
    month_year = Column(Date, nullable=False)
    rice_kg = Column(Numeric(6, 2), default=0)
    wheat_kg = Column(Numeric(6, 2), default=0)
    sugar_kg = Column(Numeric(6, 2), default=0)
    actual_offtake_rice = Column(Numeric(6, 2))
    actual_offtake_wheat = Column(Numeric(6, 2))
    fps_code = Column(String(12))
    pos_transaction_id = Column(String(50))
    source = Column(String(20))
    synced_at = Column(DateTime(timezone=True), server_default=func.now())

    ration_card = relationship("RationCard", back_populates="allocations")

class GrievanceCase(Base):
    __tablename__ = "grievance_cases"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    case_number = Column(String(25), unique=True, nullable=False)
    ration_card_id = Column(UUID(as_uuid=True), ForeignKey("ration_cards.id"))
    reporter_type = Column(String(20))
    reporter_phone_encrypted = Column(Text)
    fps_code = Column(String(12), nullable=False, index=True)
    district_code = Column(String(6), nullable=False, index=True)
    block_code = Column(String(10), nullable=False)
    issue_type = Column(String(30))
    reported_month_year = Column(Date, nullable=False)
    expected_wheat_kg = Column(Numeric(6, 2))
    expected_rice_kg = Column(Numeric(6, 2))
    received_wheat_kg = Column(Numeric(6, 2))
    received_rice_kg = Column(Numeric(6, 2))
    voice_testimony_r2_key = Column(Text)
    transcript = Column(Text)
    status = Column(String(25), default='open', index=True)
    resolution_notes = Column(Text)
    government_ref_number = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    ration_card = relationship("RationCard", back_populates="grievances")

class IvrSession(Base):
    __tablename__ = "ivr_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    twilio_call_sid = Column(String(50), unique=True)
    caller_phone_hash = Column(String(64))
    channel = Column(String(30))
    current_state = Column(String(50))
    resolved_card_id = Column(UUID(as_uuid=True), ForeignKey("ration_cards.id"), nullable=True)
    language_selected = Column(String(5), default='hi')
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    ended_at = Column(DateTime(timezone=True))
    call_duration_seconds = Column(Integer)
    is_successful = Column(Boolean, default=False)

class FpsRiskScore(Base):
    __tablename__ = "fps_risk_scores"

    fps_code = Column(String(12), primary_key=True)
    district_code = Column(String(6), nullable=False)
    block_code = Column(String(10), nullable=False)
    fps_name = Column(Text)
    complaints_30d = Column(Integer, default=0)
    complaints_90d = Column(Integer, default=0)
    resolution_rate = Column(Numeric(5, 2), default=100)
    pos_anomaly_score = Column(Numeric(5, 2), default=0)
    composite_risk_score = Column(Numeric(5, 2), default=0)
    risk_tier = Column(String(10), default='low')
    last_calculated_at = Column(DateTime(timezone=True), server_default=func.now())

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_hash = Column(String(64), unique=True, nullable=False)
    phone_encrypted = Column(Text, nullable=False)
    name = Column(Text)
    role = Column(String(30))
    district_code = Column(String(6))
    block_code = Column(String(10))
    is_active = Column(Boolean, default=True)
    last_login_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
