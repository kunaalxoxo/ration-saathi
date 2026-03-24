from typing import Dict, Any, Tuple; from upstash_redis import Redis; from app.core.config import settings; import json

class IvrFlowEngine:
    def __init__(self): self.redis = Redis(url=settings.UPSTASH_REDIS_REST_URL, token=settings.UPSTASH_REDIS_REST_TOKEN); self.ttl = 1800
    async def get_session(self, sid: str) -> Dict[str, Any]:
        s = self.redis.get(f"ivr:session:{sid}"); return json.loads(s) if s else {"call_sid": sid, "state": "CALL_RECEIVED", "language": "hi", "card_number": None, "retry_count": 0, "history": []}
    async def save_session(self, sid: str, data: Dict[str, Any]): self.redis.set(f"ivr:session:{sid}", json.dumps(data), ex=self.ttl)
    async def process_input(self, sid: str, digits: str) -> Tuple[str, str, bool]:
        s = await self.get_session(sid); cur = s["state"]
        if digits == "0":
            s["state"] = "ASSISTED_REDIRECT"; await self.save_session(sid, s)
            from app.services.entitlement import get_simple_prompt; return "ASSISTED_REDIRECT", get_simple_prompt("ASSISTED_REDIRECT", s["language"]), False
        nxt, p, g = cur, "", True
        if cur == "CALL_RECEIVED": nxt = "LANGUAGE_SELECT"
        elif cur == "LANGUAGE_SELECT":
            if digits == "1": s["language"] = "hi"; nxt = "RATION_CARD_INPUT"
            elif digits == "2": s["language"] = "raj"; nxt = "RATION_CARD_INPUT"
            else: nxt = "LANGUAGE_SELECT"
        elif cur == "RATION_CARD_INPUT":
            if len(digits) >= 6: s["card_number"] = digits; nxt = "ENTITLEMENT_READ"
            else: nxt = "RATION_CARD_INPUT"
        elif cur == "ENTITLEMENT_READ":
            if digits == "1": nxt = "CALL_COMPLETED"; g = False
            elif digits == "2": nxt = "COMPLAINT_TYPE"
        elif cur == "COMPLAINT_TYPE":
            if digits in ["1", "2", "3"]: s["issue_type"] = {"1": "wheat", "2": "rice", "3": "both"}[digits]; nxt = "QUANTITY_INPUT"
            else: nxt = "COMPLAINT_TYPE"
        elif cur == "QUANTITY_INPUT": s["received_kg"] = digits; nxt = "CASE_CREATED"; g = False
        s["state"] = nxt; await self.save_session(sid, s)
        from app.services.entitlement import get_entitlement_voice_script, get_simple_prompt
        if nxt == "ENTITLEMENT_READ":
            p = get_entitlement_voice_script(s["card_number"], s["language"])
            if p == "CARD_NOT_FOUND": nxt = "CARD_NOT_FOUND"; s["state"] = nxt; await self.save_session(sid, s); p = get_simple_prompt("CARD_NOT_FOUND", s["language"])
        elif nxt == "CASE_CREATED": p = get_simple_prompt("CASE_CREATED", s["language"]).format(case_number="RS-RJ-1234")
        elif nxt == "ASSISTED_REDIRECT": p = get_simple_prompt("ASSISTED_REDIRECT", s["language"]).format(csc_phone="9876543210")
        else: p = get_simple_prompt(nxt, s["language"])
        return nxt, p, g

flow_engine = IvrFlowEngine()
