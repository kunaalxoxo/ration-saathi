#!/usr/bin/env python3
"""
AGI Script for Ration Saathi Asterisk fallback
Communicates with the FastAPI backend to perform IVR functions
"""

import sys
import os
import json
import logging
import requests
from asterisk.agi import AGI

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/var/log/asterisk/agi-handler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configuration
BACKEND_URL = os.environ.get('BACKEND_URL', 'http://localhost:8000')
API_KEY = os.environ.get('API_KEY', '')  # For secured endpoints

def main():
    agi = AGI()
    request = agi.env
    
    # Get command line arguments
    if len(sys.argv) < 2:
        agi.verbose("No command provided", 1)
        sys.exit(1)
    
    command = sys.argv[1]
    
    # Extract call information
    call_sid = request.get('agi_channel', '').replace(' ', '_')
    caller_id = request.get('agi_callerid', '')
    
    logger.info(f"AGI script called with command: {command}, call_sid: {call_sid}, caller_id: {caller_id}")
    
    try:
        if command == 'lookup_card':
            handle_lookup_card(agi, call_sid, caller_id)
        elif command == 'get_entitlement_script':
            handle_get_entitlement_script(agi, call_sid, caller_id)
        elif command == 'announce_case_created':
            handle_announce_case_created(agi, call_sid, caller_id)
        else:
            agi.verbose(f"Unknown command: {command}", 1)
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error in AGI script: {str(e)}", exc_info=True)
        agi.verbose(f"Error in AGI script: {str(e)}", 1)
        sys.exit(1)

def handle_lookup_card(agi, call_sid, caller_id):
    """Lookup ration card by querying the backend"""
    # In a real implementation, we would have collected the card number during the IVR flow
    # For simplicity in this example, we'll simulate the lookup
    # In production, this would:
    # 1. Get the collected card number from AGI variables or a database
    # 2. Call the backend to validate the card
    # 3. Set a lookup result variable
    
    # Simulate getting card number (in reality, this would come from previous AGI steps)
    card_number = "RJ-BA-2025-00001"  # Placeholder - would be dynamically determined
    
    try:
        # Call backend to lookup card
        response = requests.get(
            f"{BACKEND_URL}/api/v1/ration-card/{card_number}",
            timeout=10
        )
        
        if response.status_code == 200:
            card_data = response.json()
            agi.set_variable("LOOKUP_RESULT", "found")
            agi.set_variable("RESOLVED_CARD_ID", card_data.get('id', ''))
            agi.set_variable("CARD_NUMBER", card_number)
            # Store other relevant data as needed
            agi.set_variable("HEAD_NAME", card_data.get('household_head_name', ''))
            agi.set_variable("EXPECTED_WHEAT_KG", str(card_data.get('expected_wheat_kg', 0)))
            agi.set_variable("EXPECTED_RICE_KG", str(card_data.get('expected_rice_kg', 0)))
            logger.info(f"Card lookup successful for {card_number}")
        else:
            agi.set_variable("LOOKUP_RESULT", "not_found")
            logger.warning(f"Card lookup failed for {card_number}: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Backend connection error during card lookup: {str(e)}")
        agi.set_variable("LOOKUP_RESULT", "error")
    except Exception as e:
        logger.error(f"Unexpected error during card lookup: {str(e)}")
        agi.set_variable("LOOKUP_RESULT", "error")

def handle_get_entitlement_script(agi, call_sid, caller_id):
    """Get entitlement script from backend"""
    # Get the resolved card ID from previous step
    resolved_card_id = agi.get_variable("RESOLVED_CARD_ID")
    if not resolved_card_id:
        logger.error("No resolved card ID available")
        agi.set_variable("ENTITLEMENT_SCRIPT", "")
        return
    
    # Get language preference (would be set during language selection)
    language = agi.get_variable("LANGUAGE_SELECTED", "hi")
    
    try:
        # Call backend to get entitlement script
        response = requests.get(
            f"{BACKEND_URL}/api/v1/entitlement-script",
            params={
                "card_id": resolved_card_id,
                "language": language
            },
            timeout=10
        )
        
        if response.status_code == 200:
            script_data = response.json()
            script_text = script_data.get('script', '')
            
            # In a real implementation, we would:
            # 1. Convert the script text to speech using TTS (Bhashini or gTTS)
            # 2. Save the audio file
            # 3. Set the path to play
            
            # For this example, we'll just set a placeholder
            # In production, you'd generate and save the audio file
            agi.set_variable("ENTITLEMENT_SCRIPT", "custom/entitlement-script")
            logger.info(f"Entitlement script retrieved for card {resolved_card_id}")
        else:
            agi.set_variable("ENTITLEMENT_SCRIPT", "")
            logger.warning(f"Failed to get entitlement script: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Backend connection error during entitlement script retrieval: {str(e)}")
        agi.set_variable("ENTITLEMENT_SCRIPT", "")
    except Exception as e:
        logger.error(f"Unexpected error during entitlement script retrieval: {str(e)}")
        agi.set_variable("ENTITLEMENT_SCRIPT", "")

def handle_announce_case_created(agi, call_sid, caller_id):
    """Announce case number and offer callback"""
    # Get collected data from previous steps
    case_number = agi.get_variable("CASE_NUMBER", "UNKNOWN")
    language = agi.get_variable("LANGUAGE_SELECTED", "hi")
    
    try:
        # In a real implementation, we would:
        # 1. Create a case via backend API using collected data
        # 2. Get the actual case number from the response
        # 3. Generate announcement audio
        
        # For this example, we'll use the case number from variables
        # In production, you'd actually create the case first
        
        # Prepare announcement text
        if language == 'hi':
            announcement_text = f"Aapki fariyaad darj ho gayi. Case number hai {case_number}. Yeh number apne paas rakhein. SMS bhi aayega. Dhanyavaad."
        else:
            announcement_text = f"Your complaint has been registered. Case number is {case_number}. Keep this number with you. You will also receive an SMS. Thank you."
        
        # In production, convert announcement_text to speech and save as audio file
        # For now, set a placeholder
        agi.set_variable("CASE_ANNOUNCEMENT", "custom/case-created")
        agi.set_variable("CASE_NUMBER_ANNOUNCED", case_number)
        logger.info(f"Case announcement prepared for case {case_number}")
        
    except Exception as e:
        logger.error(f"Error preparing case announcement: {str(e)}")
        agi.set_variable("CASE_ANNOUNCEMENT", "")

if __name__ == "__main__":
    main()
