from typing import Dict, Any, Optional, Tuple
from app.core.redis_client import redis_client
from datetime import datetime
import json, logging

logger = logging.getLogger(__name__)


class IVRStateMachine:
    def __init__(self):
        self.states = {
            "CALL_RECEIVED": {"prompt_key": None, "valid_digits": [], "next_state_map": {"": "LANGUAGE_SELECT"}},
            "LANGUAGE_SELECT": {"prompt_key": "LANGUAGE_SELECT", "valid_digits": ["0","1","2"], "next_state_map": {"0":"ASSISTED_REDIRECT","1":"RATION_CARD_INPUT","2":"RATION_CARD_INPUT","timeout":"ASSISTED_REDIRECT","invalid":"LANGUAGE_SELECT"}},
            "RATION_CARD_INPUT": {"prompt_key": "RATION_CARD_INPUT", "valid_digits": [str(i) for i in range(10)]+["*"], "next_state_map": {"timeout":"ASSISTED_REDIRECT","invalid":"RATION_CARD_INPUT"}},
            "CARD_LOOKUP": {"prompt_key": None, "valid_digits": [], "next_state_map": {"found":"ENTITLEMENT_READ","not_found":"CARD_NOT_FOUND"}},
            "ENTITLEMENT_READ": {"prompt_key": "ENTITLEMENT_READ", "valid_digits": ["1","2"], "next_state_map": {"1":"CALL_COMPLETED","2":"COMPLAINT_TYPE","timeout":"ASSISTED_REDIRECT","invalid":"ENTITLEMENT_READ"}},
            "COMPLAINT_TYPE": {"prompt_key": "COMPLAINT_TYPE", "valid_digits": ["1","2","3"], "next_state_map": {"1":"QUANTITY_INPUT","2":"QUANTITY_INPUT","3":"QUANTITY_INPUT","timeout":"ASSISTED_REDIRECT","invalid":"COMPLAINT_TYPE"}},
            "QUANTITY_INPUT": {"prompt_key": "QUANTITY_INPUT", "valid_digits": [str(i) for i in range(10)]+["*"], "next_state_map": {"timeout":"ASSISTED_REDIRECT","invalid":"QUANTITY_INPUT"}},
            "CASE_CREATED": {"prompt_key": "CASE_CREATED", "valid_digits": [], "next_state_map": {"": "CALLBACK_OFFER"}},
            "CALLBACK_OFFER": {"prompt_key": None, "valid_digits": ["1","2"], "next_state_map": {"1":"CALL_COMPLETED","2":"CALL_COMPLETED","timeout":"CALL_COMPLETED","invalid":"CALLBACK_OFFER"}},
            "CARD_NOT_FOUND": {"prompt_key": "CARD_NOT_FOUND", "valid_digits": ["0"], "next_state_map": {"0":"ASSISTED_REDIRECT","timeout":"ASSISTED_REDIRECT","invalid":"CARD_NOT_FOUND"}},
            "ASSISTED_REDIRECT": {"prompt_key": "ASSISTED_REDIRECT", "valid_digits": [], "next_state_map": {"": "CALL_COMPLETED"}},
            "CALL_COMPLETED": {"prompt_key": "CALL_COMPLETED", "valid_digits": [], "next_state_map": {"": "CALL_COMPLETED"}}
        }

    def _ts(self): return datetime.utcnow().isoformat() + "Z"

    async def get_session(self, call_sid: str) -> Optional[Dict]:
        try:
            data = await redis_client.get(f"ivr:session:{call_sid}")
            return json.loads(data) if data else None
        except Exception as e:
            logger.error("get_session error: %s", e); return None

    async def save_session(self, call_sid: str, session: Dict) -> bool:
        try:
            return await redis_client.setex(f"ivr:session:{call_sid}", 1800, json.dumps(session))
        except Exception as e:
            logger.error("save_session error: %s", e); return False

    async def create_session(self, call_sid: str, phone_hash: str, channel: str) -> Dict:
        s = {"twilio_call_sid": call_sid, "caller_phone_hash": phone_hash, "channel": channel,
             "current_state": "CALL_RECEIVED", "resolved_card_id": None, "language_selected": "hi",
             "menu_level": 0, "started_at": self._ts(), "last_active_at": self._ts(),
             "ended_at": None, "call_duration_seconds": 0, "is_successful": False, "collected_data": {}}
        await self.save_session(call_sid, s)
        return s

    async def process_input(self, call_sid: str, digit: Optional[str]) -> Tuple[str, str, Dict]:
        session = await self.get_session(call_sid)
        if not session:
            session = await self.create_session(call_sid, "unknown", "ivr_inbound")
        session["last_active_at"] = self._ts()
        state = session["current_state"]
        cfg = self.states.get(state, {})

        if state == "LANGUAGE_SELECT" and digit in ["1","2"]:
            session["language_selected"] = "hi" if digit == "1" else "raj"

        if state == "RATION_CARD_INPUT":
            if digit and digit.isdigit():
                session["collected_data"]["card_number"] = session["collected_data"].get("card_number","") + digit
                next_state = state
            elif digit == "*":
                next_state = "CARD_LOOKUP"
            else:
                next_state = cfg.get("next_state_map",{}).get("invalid", state)
        elif state == "QUANTITY_INPUT":
            if digit and digit.isdigit():
                session["collected_data"]["quantity"] = session["collected_data"].get("quantity","") + digit
                next_state = state
            elif digit == "*":
                next_state = "CASE_CREATED"
            else:
                next_state = cfg.get("next_state_map",{}).get("invalid", state)
        elif state == "COMPLAINT_TYPE" and digit in ["1","2","3"]:
            session["collected_data"]["issue_type"] = {"1":"wheat","2":"rice","3":"both"}[digit]
            next_state = cfg["next_state_map"].get(digit, state)
        else:
            next_state = cfg.get("next_state_map",{}).get(digit or "", cfg.get("next_state_map",{}).get("invalid", state))

        session["current_state"] = next_state
        prompt_key = self.states.get(next_state, {}).get("prompt_key") or next_state
        await self.save_session(call_sid, session)
        return next_state, prompt_key, session


_engine = IVRStateMachine()

async def get_session(call_sid): return await _engine.get_session(call_sid)
async def save_session(call_sid, s): return await _engine.save_session(call_sid, s)
async def create_session(call_sid, phone_hash, channel): return await _engine.create_session(call_sid, phone_hash, channel)
async def process_input(call_sid, digit): return await _engine.process_input(call_sid, digit)
