from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from app.core.config import settings
from app.ivr.flow_engine import process_input, create_session
from app.services.entitlement import get_entitlement_voice_script
from app.core.encryption import hash_for_lookup
from datetime import date
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/inbound")
async def ivr_inbound(request: Request):
    form = await request.form()
    call_sid = form.get("CallSid")
    if not call_sid: raise HTTPException(status_code=400, detail="Missing CallSid")
    phone_hash = hash_for_lookup(form.get("From", ""))
    await create_session(call_sid, phone_hash, "ivr_inbound")
    await process_input(call_sid, None)
    r = VoiceResponse()
    g = Gather(input='dtmf', action=f'/ivr/gather?call_sid={call_sid}', method='POST', timeout=8, num_digits=1)
    g.say("Ration Saathi mein aapka swagat hai. Hindi ke liye 1 dabayein. Rajasthani ke liye 2 dabayein. CSC sahayak ke liye 0 dabayein.", language='hi-IN')
    r.append(g); r.redirect('/ivr/inbound', method='POST')
    return Response(content=str(r), media_type="application/xml")


@router.post("/gather")
async def ivr_gather(request: Request, call_sid: str):
    form = await request.form()
    digit = (form.get("Digits") or "")[:1] or None
    next_state, prompt_key, session = await process_input(call_sid, digit)
    lang = session.get("language_selected", "hi")
    lc = "hi-IN"
    r = VoiceResponse()

    if next_state == "ENTITLEMENT_READ":
        card = session.get("collected_data", {}).get("card_number", "")
        today = date.today()
        script = await get_entitlement_voice_script(card, lang, date(today.year, today.month, 1))
        g = Gather(input='dtmf', action=f'/ivr/gather?call_sid={call_sid}', method='POST', timeout=8, num_digits=1)
        g.say(script, language=lc); r.append(g)
    elif next_state == "COMPLAINT_TYPE":
        g = Gather(input='dtmf', action=f'/ivr/gather?call_sid={call_sid}', method='POST', timeout=8, num_digits=1)
        g.say("Kaunsi cheez kam mili? Gehu ke liye 1, chawal ke liye 2, dono ke liye 3 dabayein.", language=lc)
        r.append(g)
    elif next_state == "QUANTITY_INPUT":
        g = Gather(input='dtmf', action=f'/ivr/gather?call_sid={call_sid}', method='POST', timeout=10, finish_on_key='*')
        g.say("Kitna mila? Kilo mein number dabayein phir star (*) dabayein.", language=lc)
        r.append(g)
    elif next_state == "CASE_CREATED":
        cn = session.get("collected_data", {}).get("case_number", "RS-XX-2025-000001")
        r.say(f"Aapki fariyaad darj ho gayi. Case number hai {cn}. SMS bhi aayega. Dhanyavaad.", language=lc)
        r.hangup()
    elif next_state == "ASSISTED_REDIRECT":
        r.say("Kripya nearest CSC kendra par jaayein.", language=lc); r.hangup()
    elif next_state == "CALL_COMPLETED":
        r.say("Ration Saathi mein call karne ke liye dhanyavaad. Jai Hind.", language=lc); r.hangup()
    else:
        g = Gather(input='dtmf', action=f'/ivr/gather?call_sid={call_sid}', method='POST', timeout=8, num_digits=1)
        g.say("Kripya button dabayein.", language=lc); r.append(g)

    return Response(content=str(r), media_type="application/xml")


@router.post("/hangup")
async def ivr_hangup(request: Request):
    return Response(content="<Response/>", media_type="application/xml")

@router.post("/missed-call")
async def ivr_missed_call(request: Request):
    return Response(content="<Response/>", media_type="application/xml")
