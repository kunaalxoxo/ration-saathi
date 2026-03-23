from typing import Dict, Any
from datetime import date
import logging
from app.db.models import GrievanceCase, RationCard
from app.db.session import get_db
from app.core.redis_client import redis_client
from app.services.sms import send_case_created_sms
from app.services.analytics import update_fps_risk_score
from app.core.encryption import decrypt

logger = logging.getLogger(__name__)


async def create_grievance_case(session_data: Dict[str, Any]) -> Dict[str, Any]:
    db = next(get_db())
    try:
        ration_card_id = session_data.get("resolved_card_id")
        if not ration_card_id:
            return {"success": False, "data": None, "error": "No ration card resolved in session"}
        card = db.query(RationCard).filter(RationCard.id == ration_card_id).first()
        if not card:
            return {"success": False, "data": None, "error": f"Ration card not found: {ration_card_id}"}

        collected = session_data.get("collected_data", {})
        grain = collected.get("issue_type", "wheat")
        exp_wheat = float(collected.get("expected_wheat_kg", 5.0))
        exp_rice = float(collected.get("expected_rice_kg", 5.0))
        try: qty = float(collected.get("quantity", "0"))
        except: qty = 0.0

        if grain == "wheat": rec_wheat, rec_rice = qty, exp_rice
        elif grain == "rice": rec_wheat, rec_rice = exp_wheat, qty
        else: rec_wheat, rec_rice = max(0.0, exp_wheat - qty/2), max(0.0, exp_rice - qty/2)

        try: seq = await redis_client.incr("grievance_case:counter") or 1
        except: import time; seq = int(time.time()) % 999999

        case_number = f"RS-{card.state_code}-{date.today().year}-{str(seq).zfill(6)}"
        if db.query(GrievanceCase).filter(GrievanceCase.case_number == case_number).first():
            case_number = f"RS-{card.state_code}-{date.today().year}-{str(seq+1).zfill(6)}"

        new_case = GrievanceCase(
            case_number=case_number, ration_card_id=ration_card_id,
            reporter_type="self", reporter_phone_encrypted=card.phone_encrypted,
            fps_code=card.fps_code, district_code=card.district_code, block_code=card.block_code,
            issue_type="short_supply", reported_month_year=date.today().replace(day=1),
            expected_wheat_kg=exp_wheat, expected_rice_kg=exp_rice,
            received_wheat_kg=rec_wheat, received_rice_kg=rec_rice, status="open"
        )
        db.add(new_case); db.commit(); db.refresh(new_case)
        logger.info("Created case %s", case_number)

        if card.phone_encrypted:
            try:
                phone = decrypt(card.phone_encrypted)
                await send_case_created_sms(phone, case_number, session_data.get("language_selected","hi"))
            except Exception as e:
                logger.error("SMS failed: %s", e)

        try: await update_fps_risk_score(card.fps_code)
        except Exception as e: logger.error("Risk score update failed: %s", e)

        return {"success": True, "data": {
            "id": str(new_case.id), "case_number": new_case.case_number,
            "fps_code": new_case.fps_code, "status": new_case.status,
            "reported_month_year": new_case.reported_month_year.isoformat(),
            "created_at": new_case.created_at.isoformat() if new_case.created_at else None
        }, "error": None}
    except Exception as e:
        logger.error("Error creating case: %s", e)
        return {"success": False, "data": None, "error": str(e)}
    finally:
        db.close()
