from datetime import date
import json, os
from app.db.session import SessionLocal; from app.db.models import RationCard, MonthlyAllocation
from app.core.encryption import encryption_service; from app.services.epds import epds_client

def get_entitlement_voice_script(card_num: str, lang: str = 'hi', dt: date = None) -> str:
    if dt is None: dt = date.today().replace(day=1)
    db = SessionLocal()
    try:
        card = db.query(RationCard).filter(RationCard.card_number == card_num).first()
        if not card:
            remote = epds_client.get_ration_card(card_num)
            if not remote: return "CARD_NOT_FOUND"
            head = remote.head_name; alloc = epds_client.get_monthly_allocation(card_num, dt)
        else: head = encryption_service.decrypt(card.household_head_name); alloc = db.query(MonthlyAllocation).filter(MonthlyAllocation.ration_card_id == card.id, MonthlyAllocation.month_year == dt).first()
        if not alloc: return "NO_ALLOCATION_FOUND"
        p_dir = os.path.join(os.path.dirname(__file__), "..", "ivr", "prompts")
        with open(os.path.join(p_dir, f"{lang}.json"), "r", encoding='utf-8') as f: p = json.load(f)
        return p["ENTITLEMENT_READ"]["prompt_template"].format(head_name=head, month=dt.strftime("%B"), wheat_kg=float(alloc.wheat_kg), rice_kg=float(alloc.rice_kg))
    finally: db.close()

def get_simple_prompt(state: str, lang: str = 'hi') -> str:
    p_dir = os.path.join(os.path.dirname(__file__), "..", "ivr", "prompts")
    try:
        with open(os.path.join(p_dir, f"{lang}.json"), "r", encoding='utf-8') as f: p = json.load(f)
        return p[state]["prompt"]
    except: return "System error."
