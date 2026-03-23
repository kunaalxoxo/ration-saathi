# Asterisk Fallback Setup for Ration Saathi

This guide explains how to set up a self-hosted Asterisk IVR system as a fallback when Twilio credits are exhausted.

## Prerequisites

- Asterisk 16 or later installed on a server (Ubuntu/Debian recommended)
- Basic knowledge of Linux command line and Asterisk configuration
- Server with public IP address or port forwarding capability
- Domain name pointing to your server (optional but recommended)

## Installation

### On Ubuntu/Debian:

```bash
# Update system
sudo apt update
sudo apt upgrade -y

# Install Asterisk and required packages
sudo apt install -y asterisk asterisk-config libffi-dev libssl-dev python3-dev python3-pip

# Install Python AGI library
pip3 install pystagi flask
```

### Configuration Files

Copy the provided configuration files to your Asterisk configuration directory:

```bash
# Copy dialplan
sudo cp ivr-scripts/asterisk/ration_saathi.conf /etc/asterisk/extensions.d/

# Copy AGI script
sudo cp ivr-scripts/asterisk/agi_handler.py /var/lib/asterisk/agi-bin/
sudo chown asterisk:asterisk /var/lib/asterisk/agi-bin/agi_handler.py
sudo chmod +x /var/lib/asterisk/agi-bin/agi_handler.py
```

## Configuration Details

### extensions.conf (ration_saathi.conf)

This file contains the dialplan for the Ration Saathi IVR system:

```
[ration-saathi]
exten => s,1,Answer()
    same => n,Set(TIMEOUT(digit)=5)
    same => n,Set(TIMEOUT(response)=10)
    same => n,Goto(s-${EVIRONMENT(LANGUAGE_SELECT)},start,1)

; Language selection menu
exten => s-LANGUAGE_SELECT,1,Background(custom/welcome-message)
    same => n,WaitExten(5)
    same => n,GotoIf($["${EXTEN}" = ""]?s-LANGUAGE_SELECT,t,1)
    same => n,GotoIf($["${EXTEN}" = "1"]?s-RATION_CARD_INPUT,start,1)
    same => n,GotoIf($["${EXTEN}" = "2"]?s-RATION_CARD_INPUT,start,1)
    same => n,GotoIf($["${EXTEN}" = "0"]?s-ASSISTED_REDIRECT,start,1)
    same => n,Goto(s-LANGUAGE_SELECT,t,1)

exten => s-LANGUAGE_SELECT,t,1,Playback(custom/invalid-input)
    same => n,Goto(s-LANGUAGE_SELECT,start,1)

; Ration card input
exten => s-RATION_CARD_INPUT,1,Background(custom/enter-card-number)
    same => n,Read(CARD_NUMBER,,10,#,2,5)
    same => n,GotoIf($["${CARD_NUMBER}" = ""]?s-RATION_CARD_INPUT,i,1)
    same => n,Goto(s-CARD_LOOKUP,start,1)

exten => s-RATION_CARD_INPUT,i,1,Playback(custom/invalid-number)
    same => n,Goto(s-RATION_CARD_INPUT,start,1)

; Card lookup (handled by AGI)
exten => s-CARD_LOOKUP,1,AGI(agi_handler.py,lookup_card)
    same => n,GotoIf($["${LOOKUP_RESULT}" = "found"]?s-ENTITLEMENT_READ,start,1)
    same => n,Goto(s-CARD_NOT_FOUND,start,1)

; Entitlement reading
exten => s-ENTITLEMENT_READ,1,AGI(agi_handler.py,get_entitlement_script)
    same => n,Playback(custom/entitlement-script)
    same => n,WaitExten(5)
    same => n,GotoIf($["${EXTEN}" = "1"]?s-CALL_COMPLETED,start,1)
    same => n,GotoIf($["${EXTEN}" = "2"]?s-COMPLAINT_TYPE,start,1)
    same => n,Goto(s-ASSISTED_REDIRECT,start,1)

; Complaint type selection
exten => s-COMPLAINT_TYPE,1,Background(custom/select-issue-type)
    same => n,WaitExten(5)
    same => n,GotoIf($["${EXTEN}" = "1"]?s-QUANTITY_INPUT,start,1)
    same => n,GotoIf($["${EXTEN}" = "2"]?s-QUANTITY_INPUT,start,1)
    same => n,GotoIf($["${EXTEN}" = "3"]?s-QUANTITY_INPUT,start,1)
    same => n,Goto(s-ASSISTED_REDIRECT,start,1)

exten => s-COMPLAINT_TYPE,t,1,Playback(custom/invalid-input)
    same => n,Goto(s-COMPLAINT_TYPE,start,1)

; Quantity input
exten => s-QUANTITY_INPUT,1,Background(custom/enter-quantity)
    same => n,Read(QUANTITY,,5,*,2,10)
    same => n,GotoIf($["${QUANTITY}" = ""]?s-QUANTITY_INPUT,i,1)
    same => n,Goto(s-CASE_CREATED,start,1)

exten => s-QUANTITY_INPUT,i,1,Playback(custom/invalid-quantity)
    same => n,Goto(s-QUANTITY_INPUT,start,1)

; Case created announcement
exten => s-CASE_CREATED,1,AGI(agi_handler.py,announce_case_created)
    same => n,Playback(custom/case-created)
    same => n,WaitExten(5)
    same => n,Goto(s-CALLBACK_OFFER,start,1)

; Callback offer
exten => s-CALLBACK_OFFER,1,Background(custom/callback-offer)
    same => n,WaitExten(5)
    same => n,GotoIf($["${EXTEN}" = "1"]?s-CALL_COMPLETED,start,1)
    same => n,GotoIf($["${EXTEN}" = "2"]?s-CALL_COMPLETED,start,1)
    same => n,Goto(s-CALL_COMPLETED,start,1)

; Card not found
exten => s-CARD_NOT_FOUND,1,Playback(custom/card-not-found)
    same => n,WaitExten(5)
    same => n,Goto(s-ASSISTED_REDIRECT,start,1)

; Assisted redirect
exten => s-ASSISTED_REDIRECT,1,Playback(custom/assisted-redirect)
    same => n,Hangup()

; Call completed
exten => s-CALL_COMPLETED,1,Playback(custom/thank-you)
    same => n,Hangup()

; Missing call handling
exten => s,2,Hangup()
```

### AGI Script (agi_handler.py)

The AGI script handles all the business logic by communicating with the FastAPI backend:

```python
#!/usr/bin/env python3
"""
AGI Script for Ration Saathi Asterisk fallback
Communicates with the FastAPI backend to perform IVR functions
"""

import sys
import os
import json
import requests
from asterisk.agi import AGI

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
        agi.verbose(f"Error in AGI script: {str(e)}", 1)
        sys.exit(1)

def handle_lookup_card(agi, call_sid, caller_id):
    """Lookup ration card by querying the backend"""
    # In a real implementation, we would collect digits until #
    # For simplicity, we'll assume the card number was already collected
    # and stored in a variable or we need to re-prompt
    
    # This would typically involve:
    # 1. Getting the collected card number from a database or session
    # 2. Calling the backend to validate the card
    # 3. Setting a lookup result variable
    
    # Placeholder implementation
    agi.set_variable("LOOKUP_RESULT", "not_found")
    
    # In reality:
    # response = requests.get(f"{BACKEND_URL}/api/v1/ration-card/{card_number}")
    # if response.status_code == 200:
    #     agi.set_variable("LOOKUP_RESULT", "found")
    #     agi.set_variable("RESOLVED_CARD_ID", response.json()['id'])
    # else:
    #     agi.set_variable("LOOKUP_RESULT", "not_found")

def handle_get_entitlement_script(agi, call_sid, caller_id):
    """Get entitlement script from backend"""
    # Similar to lookup, this would:
    # 1. Get the resolved card ID from previous step
    # 2. Call backend to get entitlement script
    # 3. Save the script as a audio file to play
    
    # Placeholder - would generate and save audio file
    agi.verbose("Getting entitlement script", 1)

def handle_announce_case_created(agi, call_sid, caller_id):
    """Announce case number and offer callback"""
    # Similar to above - would:
    # 1. Create a case via backend API
    # 2. Get the case number
    # 3. Generate audio announcement
    # 4. Offer callback option
    
    agi.verbose("Announcing case created", 1)

if __name__ == "__main__":
    main()
```

## Audio Prompts

You'll need to record or generate audio prompts for all the IVR prompts. Place them in `/var/lib/asterisk/sounds/custom/` or another directory referenced in the dialplan.

Required prompts:
- welcome-message.gsm
- enter-card-number.gsm
- invalid-number.gsm
- invalid-input.gsm
- entitlement-script.gsm (dynamic)
- select-issue
