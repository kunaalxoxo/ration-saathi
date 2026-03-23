# FILE: ration-saathi/backend/app/api/ivr_webhook.py
from fastapi import APIRouter, Request, HTTPException, Form
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather, Say, Pause
from twilio.request_validator import RequestValidator
from app.core.config import settings
from app.ivr.flow_engine import process_input, create_session
from app.services.entitlement import get_entitlement_voice_script
from app.services.groq_client import generate_resolution_explanation
from app.db.models import GrievanceCase
from sqlalchemy.orm import Session
from app.db.session import get_db
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize Twilio request validator
validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)

def validate_twilio_request(request: Request) -> bool:
    """
    Validate that the request came from Twilio
    """
    # Get the signature from headers
    signature = request.headers.get('X-Twilio-Signature', '')
    
    # Get the URL and form data
    url = str(request.url)
    form_data = {}
    
    # For POST requests, we need to get the form data
    # Note: In a real implementation, we would await request.form()
    # But for validation, we need the raw data
    # This is a simplified version - in production, you'd need to handle this properly
    
    # For now, we'll return True in development to allow testing
    if settings.ENVIRONMENT == "development":
        return True
    
    # In production, we would properly validate
    # This is a placeholder for the actual validation logic
    return True

@router.post("/inbound")
async def ivr_inbound(request: Request):
    """
    Handle incoming Twilio calls
    """
    # Validate Twilio request (skip in development for testing)
    if not validate_twilio_request(request):
        logger.warning("Invalid Twilio request signature")
        raise HTTPException(status_code=403, detail="Invalid Twilio signature")
    
    # Parse form data
    form_data = await request.form()
    call_sid = form_data.get("CallSid")
    caller_number = form_data.get("From", "")
    
    if not call_sid:
        logger.error("No CallSid in Twilio request")
        raise HTTPException(status_code=400, detail="Missing CallSid")
    
    # Create a hash of the caller's phone number for privacy
    from app.core.encryption import hash_for_lookup
    caller_phone_hash = hash_for_lookup(caller_number)
    
    # Create new IVR session
    session = await create_session(call_sid, caller_phone_hash, "ivr_inbound")
    
    # Get the language select prompt
    next_state, prompt_key, updated_session = await process_input(call_sid, None)
    
    # Generate TwiML response
    response = VoiceResponse()
    
    if prompt_key:
        # Get the prompt text from our prompt files
        # In a real implementation, we would load this from JSON files based on language
        # For now, we'll use a hardcoded Hindi prompt
        prompt_text = "Ration Saathi mein aapka swagat hai. Hindi ke liye 1 dabayein. Rajasthani ke liye 2 dabayein. CSC sahayak ke liye 0 dabayein."
        
        gather = Gather(
            input='dtmf',
            action=f'/ivr/gather?call_sid={call_sid}',
            method='POST',
            timeout=5,
            num_digits=1
        )
        gather.say(prompt_text, language='hi-IN')
        response.append(gather)
        
        # Add a pause and redirect if no input
        response.pause(length=10)
        response.redirect(f'/ivr/gather?call_sid={call_sid}', method='POST')
    else:
        # Fallback
        response.say("Ration Saathi mein aapka swagat hai.", language='hi-IN')
        response.redirect('/ivr/inbound', method='POST')
    
    return Response(content=str(response), media_type="application/xml")

@router.post("/gather")
async def ivr_gather(request: Request, call_sid: str):
    """
    Handle Gather input from Twilio
    """
    # Validate Twilio request (skip in development for testing)
    if not validate_twilio_request(request):
        logger.warning("Invalid Twilio request signature")
        raise HTTPException(status_code=403, detail="Invalid Twilio signature")
    
    # Parse form data
    form_data = await request.form()
    digits = form_data.get("Digits", "")
    
    logger.info(f"Received digits '{digits}' for call {call_sid}")
    
    # Process the input
    # If digits is empty, it means timeout or no input
    digit = digits[0] if digits else None
    
    next_state, prompt_key, session = await process_input(call_sid, digit)
    
    # Generate TwiML response based on the state
    response = VoiceResponse()
    
    # Handle special states that need dynamic data
    if next_state == "ENTITLEMENT_READ":
        # Get entitlement data for the voice script
        # In a real implementation, we would get the card number from session
        card_number = session.get("collected_data", {}).get("card_number", "")
        language = session.get("language_selected", "hi")
        
        # Get the entitlement voice script
        # We would need the month - for now use current month
        from datetime import date
        today = date.today()
        month_year = date(today.year, today.month, 1)  # First day of current month
        
        voice_script = await get_entitlement_voice_script(card_number, language, month_year)
        
        gather = Gather(
            input='dtmf',
            action=f'/ivr/gather?call_sid={call_sid}',
            method='POST',
            timeout=5,
            num_digits=1
        )
        gather.say(voice_script, language='hi-IN' if language == 'hi' else 'hi-IN')
        response.append(gather)
        
        # Add timeout handling
        response.pause(length=10)
        response.redirect(f'/ivr/gather?call_sid={call_sid}', method='POST')
        
    elif next_state == "QUANTITY_INPUT":
        # Get expected quantity for the prompt
        # In a real implementation, we would get this from session or entitlement data
        expected_kg = session.get("collected_data", {}).get("expected_kg", 5.0)
        language = session.get("language_selected", "hi")
        
        if language == 'hi':
            prompt_text = f"Aapko {expected_kg} kilo milna chahiye tha. Kitna mila? Kilo mein number dabayein phir star (*)."
        else:
            prompt_text = f"You should have received {expected_kg} kg. How much did you get? Enter number in kilos then press star."
        
        gather = Gather(
            input='dtmf',
            action=f'/ivr/gather?call_sid={call_sid}',
            method='POST',
            timeout=10,
            finish_on_key='*'
        )
        gather.say(prompt_text, language='hi-IN' if language == 'hi' else 'en-US')
        response.append(gather)
        
        # Add timeout handling
        response.pause(length=15)
        response.redirect(f'/ivr/gather?call_sid={call_sid}', method='POST')
        
    elif next_state == "CASE_CREATED":
        # Get case number from session (would be generated in real implementation)
        case_number = session.get("collected_data", {}).get("case_number", "RS-XX-2025-XXXX")
        language = session.get("language_selected", "hi")
        
        if language == 'hi':
            prompt_text = f"Aapki fariyaad darj ho gayi. Case number hai {case_number}. Yeh number apne paas rakhein. SMS bhi aayega. Dhanyavaad."
        else:
            prompt_text = f"Your complaint has been registered. Case number is {case_number}. Keep this number with you. You will also receive an SMS. Thank you."
        
        response.say(prompt_text, language='hi-IN' if language == 'hi' else 'en-US')
        response.pause(length=5)
        # After announcing case created, offer callback
        gather = Gather(
            input='dtmf',
            action=f'/ivr/gather?call_sid={call_sid}',
            method='POST',
            timeout=5,
            num_digits=1
        )
        gather.say("Kya aapke liye callback chahiye? Haan ke liye 1, nahin ke liye 2 dabayein.", language='hi-IN')
        response.append
