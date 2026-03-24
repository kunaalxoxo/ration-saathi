import pytest; from app.ivr.flow_engine import flow_engine
@pytest.mark.asyncio
async def test_flow():
    sid = "test_123"; st, p, g = await flow_engine.process_input(sid, "")
    assert st == "LANGUAGE_SELECT"; assert g is True
    st, p, g = await flow_engine.process_input(sid, "2"); assert st == "RATION_CARD_INPUT"
