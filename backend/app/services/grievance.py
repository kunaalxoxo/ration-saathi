from datetime import date
import uuid
from upstash_redis import Redis
from app.db.session import SessionLocal
from app.db.models import GrievanceCase
from app.core.config import settings
from app.core.encryption import encryption_service
from pydantic import BaseModel
from typing import Optional


class GrievanceCreate(BaseModel):
    ration_card_id: uuid.UUID
    reporter_type: str
    issue_type: str
    reported_month_year: date
    expected_wheat_kg: float
    expected_rice_kg: float
    received_wheat_kg: float
    received_rice_kg: float
    fps_code: str
    district_code: str
    block_code: str
    reporter_phone: Optional[str] = None


async def create_grievance_case(data: GrievanceCreate) -> GrievanceCase:
    db = SessionLocal()
    redis = Redis(
        url=settings.UPSTASH_REDIS_REST_URL,
        token=settings.UPSTASH_REDIS_REST_TOKEN
    )
    try:
        yr = date.today().year
        st = "RJ"
        key = f"seq:grievance:{st}:{yr}"
        seq = redis.incr(key)
        cn = f"RS-{st}-{yr}-{seq:05d}"
        e_p = encryption_service.encrypt(data.reporter_phone) if data.reporter_phone else None
        nc = GrievanceCase(
            case_number=cn,
            ration_card_id=data.ration_card_id,
            reporter_type=data.reporter_type,
            reporter_phone_encrypted=e_p,
            fps_code=data.fps_code,
            district_code=data.district_code,
            block_code=data.block_code,
            issue_type=data.issue_type,
            reported_month_year=data.reported_month_year,
            expected_wheat_kg=data.expected_wheat_kg,
            expected_rice_kg=data.expected_rice_kg,
            received_wheat_kg=data.received_wheat_kg,
            received_rice_kg=data.received_rice_kg,
            status="open"
        )
        db.add(nc)
        db.commit()
        db.refresh(nc)
        if data.reporter_phone:
            from app.worker import send_sms_task
            send_sms_task.delay(data.reporter_phone, cn, "hi")
        from app.worker import update_fps_risk_score_task
        update_fps_risk_score_task.delay(data.fps_code)
        return nc
    finally:
        db.close()
