from fastapi import APIRouter, Request, Response; from twilio.twiml.voice_response import VoiceResponse, Gather; from twilio.request_validator import RequestValidator; from app.core.config import settings; from app.ivr.flow_engine import flow_engine; from app.services.bhashini import bhashini_client
router = APIRouter(prefix="/ivr", tags=["ivr"])
async def validate(r: Request):
    v = RequestValidator(settings.TWILIO_AUTH_TOKEN); sig = r.headers.get("X-Twilio-Signature", ""); url = str(r.url); form = await r.form(); params = dict(form)
    if not v.validate(url, params, sig): print("Signature Validation Failed")
@router.post("/inbound")
async def inbound(r: Request):
    await validate(r); form = await r.form(); sid = form.get("CallSid")
    _, p, _ = await flow_engine.process_input(sid, "")
    res = VoiceResponse(); g = Gather(num_digits=1, action="/ivr/gather"); g.say(p, language='hi-IN'); res.append(g); return Response(content=str(res), media_type="application/xml")
@router.post("/gather")
async def gather(r: Request):
    await validate(r); form = await r.form(); sid = form.get("CallSid"); digits = form.get("Digits", "")
    nxt, p, g = await flow_engine.process_input(sid, digits); res = VoiceResponse()
    if g:
        num = 12 if nxt == "RATION_CARD_INPUT" else 1; f_key = "*" if nxt == "RATION_CARD_INPUT" else ""
        ga = Gather(num_digits=num, action="/ivr/gather", finish_on_key=f_key); ga.say(p, language='hi-IN'); res.append(ga)
    else: res.say(p, language='hi-IN'); res.hangup()
    return Response(content=str(res), media_type="application/xml")
@router.post("/hangup")
async def hangup(r: Request): return {"success": True}
