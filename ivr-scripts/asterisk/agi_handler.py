#!/usr/bin/env python3
import sys, httpx, asyncio; from asterisk.agi import AGI
agi = AGI(); BACKEND = "https://your-render-app.onrender.com/api/ivr"
async def step(sid, digits=""):
    async with httpx.AsyncClient() as c:
        r = await c.post(f"{BACKEND}/gather", json={"CallSid": sid, "Digits": digits})
        d = r.json(); agi.verbose(f"Prompt: {d.get('prompt')}")
        return agi.get_data("beep", timeout=10000, max_digits=12) if d.get("should_gather") else ""
if __name__ == "__main__":
    agi.answer(); sid = agi.env['agi_uniqueid']; inp = ""
    while True:
        inp = asyncio.run(step(sid, inp))
        if not inp: break
