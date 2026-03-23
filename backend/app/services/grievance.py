# FILE: ration-saathi/backend/app/services/grievance.py
from typing import Dict, Any, Optional
from datetime import date
import uuid
import logging
from app.db.models import GrievanceCase, RationCard
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.redis_client import redis_client
from app.services.sms import send_case_created_sms
from app.services.analytics import update_fps_risk_score  # Now we can import it since it's implemented
from app.core.encryption import encrypt, decrypt

logger = logging.getLogger(__name__)

async def create_grievance_case(session_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a grievance case from IVR session data.
    Returns the created case as a dictionary.
    Steps:
    1. Generate case number using atomic Upstash Redis INCR
    2. Store in Supabase grievance_cases table
    3. Trigger Fast2SMS: send case ID to reporter's phone (decrypt phone, send SMS)
    4. Recalculate fps_risk_scores for the relevant FPS (call analytics service)
    5. Return complete GrievanceCase Pydantic model (as dict)
    """
    db = next(get_db())
    try:
        # Extract data from session
        ration_card_id = session_data.get("resolved_card_id")
        if not ration_card_id:
            raise ValueError("No ration card resolved in session")
        
        # Get ration card details for FPS, district, block
        ration_card = db.query(RationCard).filter(RationCard.id == ration_card_id).first()
        if not ration_card:
            raise ValueError(f"Ration card not found for id {ration_card_id}")
        
        # Reporter's phone is encrypted in the ration card record
        reporter_phone_encrypted = ration_card.phone_encrypted
        
        # For the IVR flow, we collected:
        #   issue_type: from COMPLAINT_TYPE state (1=wheat, 2=rice, 3=both)
        #   quantity_received: from QUANTITY_INPUT state (the amount they received)
        # We also need the expected amount from the entitlement.
        collected_data = session_data.get("collected_data", {})
        
        # Determine which grain they are complaining about
        grain_type = collected_data.get("issue_type", "wheat")  # from our flow engine storage
        
        # Expected and received quantities
        # We'll get the expected amounts from the session (stored during ENTITLEMENT_READ)
        expected_wheat_kg = float(collected_data.get("expected_wheat_kg", 0))
        expected_rice_kg = float(collected_data.get("expected_rice_kg", 0))
        
        # Received quantity: we got this in QUANTITY_INPUT
        quantity_received_str = collected_data.get("quantity", "0")
        try:
            quantity_received = float(quantity_received_str)
        except ValueError:
            quantity_received = 0.0
        
        # Now, set received and expected based on grain type
        if grain_type == "wheat":
            received_wheat_kg = quantity_received
            received_rice_kg = expected_rice_kg  # Assume they got full rice
        elif grain_type == "rice":
            received_rice_kg = quantity_received
            received_wheat_kg = expected_wheat_kg  # Assume they got full wheat
        else:  # both
            # For both, we'll assume they reported total shortfall and split it equally
            # This is a simplification - in reality we might need separate queries
            received_wheat_kg = max(0, expected_wheat_kg - quantity_received/2)
            received_rice_kg = max(0, expected_rice_kg - quantity_received/2)
        
        # Generate case number using Upstash Redis atomic INCR
        # Key: grievance_case:counter
        # We'll format as RS-{STATE_CODE}-{YEAR}-{zero-padded-seq}
        state_code = ration_card.state_code
        # Get current year
        current_year = date.today().year
        # Get the sequence number from Redis
        sequence_key = "grievance_case:counter"
        # We need to increment and get the new value atomically.
        # Upstash Redis INCR returns the new value.
        try:
            sequence_number = await redis_client.incr(sequence_key)
            if sequence_number is None:
                # Fallback to a timestamp-based sequence if Redis fails
                sequence_number = int(date.today().strftime("%Y%m%d%H%M%S"))
        except Exception as e:
            logger.error(f"Failed to increment sequence in Redis: {str(e)}")
            # Fallback
            sequence_number = int(date.today().strftime("%Y%m%d%H%M%S"))
        
        # Format sequence number to be zero-padded to at least 6 digits
        sequence_str = str(sequence_number).zfill(6)
        case_number = f"RS-{state_code}-{current_year}-{sequence_str}"
        
        # Ensure case number is unique (check in DB)
        existing = db.query(GrievanceCase).filter(GrievanceCase.case_number == case_number).first()
        if existing:
            # Very unlikely, but if it happens, increment again
            try:
                sequence_number = await redis_client.incr(sequence_key)
            except Exception:
                sequence_number = sequence_number + 1
            sequence_str = str(sequence_number).zfill(6)
            case_number = f"RS-{state_code}-{current_year}-{sequence_str}"
        
        # Prepare case data for insertion
        case_data = {
            "case_number": case_number,
            "ration_card_id": ration_card_id,
            "reporter_type": "self",  # From IVR, it's self-reported. Could be shg_leader or csc_operator in other flows.
            "reporter_phone_encrypted": reporter_phone_encrypted,
            "fps_code": ration_card.fps_code,
            "district_code": ration_card.district_code,
            "block_code": ration_card.block_code,
            "issue_type": "short_supply",  # All cases from this flow are short_supply (less received)
            "reported_month_year": date.today().replace(day=1),  # First day of current month
            "expected_wheat_kg": expected_wheat_kg,
            "expected_rice_kg": expected_rice_kg,
            "received_wheat_kg": received_wheat_kg,
            "received_rice_kg": received_rice_kg,
            "voice_testimony_r2_key": None,  # Not captured in this IVR flow (would be optional)
            "transcript": None,  # Not captured in this IVR flow (would be from STT if we recorded)
            "status": "open",
            "resolution_notes": None,
            "government_ref_number": None
        }
        
        # Create the case object
        new_case = GrievanceCase(**case_data)
        db.add(new_case)
        db.commit()
        db.refresh(new_case)
        
        logger.info(f"Created grievance case {case_number}")
        
        # Send SMS to the reporter
        # We need to decrypt the phone number to send SMS
        reporter_phone = decrypt(reporter_phone_encrypted) if reporter_phone_encrypted else None
        if reporter_phone:
            # Get language from session
            language = session_data.get("language_selected", "hi")
            await send_case_created_sms(reporter_phone, case_number, language)
        else:
            logger.warning("Could not send SMS: reporter phone number not available")
        
        # Update FPS risk score (trigger background task)
        try:
            await update_fps_risk_score(ration_card.fps_code)
        except Exception as e:
            logger.error(f"Failed to update FPS risk score for {ration_card.fps_code}: {str(e)}")
            # Don't fail the case creation if risk score update fails
        
        # Return the case as a dictionary
        return {
            "id": str(new_case.id),
            "case_number": new_case.case_number,
            "ration_card_id": str(new_case.ration_card_id),
            "reporter_type": new_case.reporter_type,
            "fps_code": new_case.fps_code,
            "district_code": new_case.district_code,
            "block_code": new_case.block_code,
            "issue_type": new_case.issue_type,
            "reported_month_year": new_case.reported_month_year.isoformat() if new_ca
