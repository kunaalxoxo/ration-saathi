# FILE: ration-saathi/backend/app/ivr/flow_engine.py
from typing import Dict, Any, Optional, Tuple
from app.core.redis_client import redis_client
import json
import logging

logger = logging.getLogger(__name__)

class IVRStateMachine:
    def __init__(self):
        # Define the state machine configuration
        self.states = {
            "CALL_RECEIVED": {
                "prompt_key": None,  # No prompt, just transition
                "valid_digits": [],  # No input expected
                "timeout_action": "transition",
                "next_state_map": {"": "LANGUAGE_SELECT"}  # Empty string means auto-transition
            },
            "LANGUAGE_SELECT": {
                "prompt_key": "LANGUAGE_SELECT",
                "valid_digits": ["0", "1", "2"],
                "timeout_action": "repeat_once",
                "next_state_map": {
                    "0": "ASSISTED_REDIRECT",
                    "1": "RATION_CARD_INPUT",
                    "2": "RATION_CARD_INPUT",
                    "timeout": "ASSISTED_REDIRECT",
                    "invalid": "LANGUAGE_SELECT"  # Stay in same state on invalid input
                }
            },
            "RATION_CARD_INPUT": {
                "prompt_key": "RATION_CARD_INPUT",
                "valid_digits": [str(i) for i in range(10)] + ["*"],  # 0-9 and *
                "timeout_action": "repeat_once",
                "next_state_map": {
                    "timeout": "ASSISTED_REDIRECT",
                    "invalid": "RATION_CARD_INPUT"
                    # Valid card number (ending with *) will be handled separately
                }
            },
            "CARD_LOOKUP": {
                "prompt_key": None,  # No prompt, just transition
                "valid_digits": [],
                "timeout_action": "transition",
                "next_state_map": {
                    "found": "ENTITLEMENT_READ",
                    "not_found": "CARD_NOT_FOUND"
                }
            },
            "ENTITLEMENT_READ": {
                "prompt_key": "ENTITLEMENT_READ",  # Will use prompt_template
                "valid_digits": ["1", "2"],
                "timeout_action": "repeat_once",
                "next_state_map": {
                    "1": "CALL_COMPLETED",  # All received
                    "2": "COMPLAINT_TYPE",  # Less received
                    "timeout": "ASSISTED_REDIRECT",
                    "invalid": "ENTITLEMENT_READ"
                }
            },
            "COMPLAINT_TYPE": {
                "prompt_key": "COMPLAINT_TYPE",
                "valid_digits": ["1", "2", "3"],
                "timeout_action": "repeat_once",
                "next_state_map": {
                    "1": "QUANTITY_INPUT",  # Wheat
                    "2": "QUANTITY_INPUT",  # Rice
                    "3": "QUANTITY_INPUT",  # Both
                    "timeout": "ASSISTED_REDIRECT",
                    "invalid": "COMPLAINT_TYPE"
                }
            },
            "QUANTITY_INPUT": {
                "prompt_key": "QUANTITY_INPUT",  # Will use prompt_template
                "valid_digits": [str(i) for i in range(10)] + ["*"],  # 0-9 and *
                "timeout_action": "repeat_once",
                "next_state_map": {
                    "timeout": "ASSISTED_REDIRECT",
                    "invalid": "QUANTITY_INPUT"
                    # Valid quantity (ending with *) will be handled separately
                }
            },
            "CASE_CREATED": {
                "prompt_key": "CASE_CREATED",  # Will use prompt_template
                "valid_digits": [],  # No input expected
                "timeout_action": "transition",
                "next_state_map": {"": "CALLBACK_OFFER"}  # Auto-transition
            },
            "CALLBACK_OFFER": {
                "prompt_key": None,  # We'll handle this specially
                "valid_digits": ["1", "2"],
                "timeout_action": "repeat_once",
                "next_state_map": {
                    "1": "CALL_COMPLETED",  # Yes to callback
                    "2": "CALL_COMPLETED",  # No to callback
                    "timeout": "CALL_COMPLETED",
                    "invalid": "CALLBACK_OFFER"
                }
            },
            "CARD_NOT_FOUND": {
                "prompt_key": "CARD_NOT_FOUND",
                "valid_digits": ["0"],
                "timeout_action": "repeat_once",
                "next_state_map": {
                    "0": "ASSISTED_REDIRECT",
                    "timeout": "ASSISTED_REDIRECT",
                    "invalid": "CARD_NOT_FOUND"
                }
            },
            "ASSISTED_REDIRECT": {
                "prompt_key": "ASSISTED_REDIRECT",
                "valid_digits": [],  # No input expected
                "timeout_action": "transition",
                "next_state_map": {"": "CALL_COMPLETED"}  # Auto-transition
            },
            "CALL_COMPLETED": {
                "prompt_key": "CALL_COMPLETED",
                "valid_digits": [],  # No input expected
                "timeout_action": "transition",
                "next_state_map": {"": "CALL_COMPLETED"}  # Stay in completed state
            }
        }
        
        # Maximum menu levels to prevent infinite loops
        self.max_menu_levels = 3
    
    async def get_session(self, call_sid: str) -> Optional[Dict[str, Any]]:
        """Get IVR session from Redis"""
        try:
            session_data = await redis_client.get(f"ivr:session:{call_sid}")
            if session_data:
                return json.loads(session_data)
            return None
        except Exception as e:
            logger.error(f"Error getting IVR session for {call_sid}: {str(e)}")
            return None
    
    async def save_session(self, call_sid: str, session: Dict[str, Any]) -> bool:
        """Save IVR session to Redis with 30-minute TTL"""
        try:
            session_json = json.dumps(session)
            result = await redis_client.setex(
                f"ivr:session:{call_sid}",
                30 * 60,  # 30 minutes in seconds
                session_json
            )
            return result
        except Exception as e:
            logger.error(f"Error saving IVR session for {call_sid}: {str(e)}")
            return False
    
    async def create_session(self, call_sid: str, caller_phone_hash: str, channel: str) -> Dict[str, Any]:
        """Create a new IVR session"""
        session = {
            "twilio_call_sid": call_sid,
            "caller_phone_hash": caller_phone_hash,
            "channel": channel,
            "current_state": "CALL_RECEIVED",
            "resolved_card_id": None,
            "language_selected": "hi",  # Default to Hindi
            "menu_level": 0,
            "started_at": self._get_current_timestamp(),
            "last_active_at": self._get_current_timestamp(),
            "ended_at": None,
            "call_duration_seconds": 0,
            "is_successful": False,
            "collected_data": {}  # For storing data collected during the call
        }
        
        await self.save_session(call_sid, session)
        return session
    
    async def process_input(self, call_sid: str, digit: Optional[str]) -> Tuple[str, str, Dict[str, Any]]:
        """
        Process user input and return next state, prompt key, and updated session
        Returns: (next_state, prompt_key, session_data)
        """
        # Get current session
        session = await self.get_session(call_sid)
        if not session:
            # Session not found, create a new one (shouldn't happen in normal flow)
            logger.warning(f"Session not found for {call_sid}, creating new session")
            session = await self.create_session(call_sid, "unknown", "ivr_inbound")
        
        # Update last active time
        session["last_active_at"] = self._get_current_timestamp()
        
        current_state = session["current_state"]
        state_config = self.states.get(current_state)
        
        if not state_config:
            logger.error(f"Unknown state: {current_state}")
