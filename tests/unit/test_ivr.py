import pytest
from unittest.mock import MagicMock, patch
from app.ivr.flow_engine import IvrFlowEngine

@pytest.mark.asyncio
async def test_flow():
    # Setup mock Redis
    mock_redis = MagicMock()
    mock_redis.get.return_value = None
    mock_redis.set.return_value = True
    
    with patch('app.ivr.flow_engine.Redis', return_value=mock_redis), \
         patch('app.services.entitlement.get_simple_prompt', return_value="Hello"):
        
        # New instance of flow engine to use our mock
        flow_engine = IvrFlowEngine()
        
        sid = "test_123"
        # CALL_RECEIVED -> LANGUAGE_SELECT
        nxt, p, g = await flow_engine.process_input(sid, "")
        assert nxt == "LANGUAGE_SELECT"
        
        # LANGUAGE_SELECT -> RATION_CARD_INPUT
        mock_redis.get.return_value = '{"state": "LANGUAGE_SELECT", "language": "hi"}'
        nxt, p, g = await flow_engine.process_input(sid, "1")
        assert nxt == "RATION_CARD_INPUT"
        
        # RATION_CARD_INPUT -> ENTITLEMENT_READ
        mock_redis.get.return_value = '{"state": "RATION_CARD_INPUT", "language": "hi"}'
        with patch('app.services.entitlement.get_entitlement_voice_script', return_value="Your entitlement"):
            nxt, p, g = await flow_engine.process_input(sid, "123456")
            assert nxt == "ENTITLEMENT_READ"
            assert p == "Your entitlement"

        # ENTITLEMENT_READ -> COMPLAINT_TYPE
        mock_redis.get.return_value = '{"state": "ENTITLEMENT_READ", "language": "hi", "card_number": "123456"}'
        nxt, p, g = await flow_engine.process_input(sid, "2")
        assert nxt == "COMPLAINT_TYPE"

        # COMPLAINT_TYPE -> QUANTITY_INPUT
        mock_redis.get.return_value = '{"state": "COMPLAINT_TYPE", "language": "hi", "issue_type": "wheat"}'
        nxt, p, g = await flow_engine.process_input(sid, "1")
        assert nxt == "QUANTITY_INPUT"

        # QUANTITY_INPUT -> CASE_CREATED
        mock_redis.get.return_value = '{"state": "QUANTITY_INPUT", "language": "hi", "received_kg": "3"}'
        nxt, p, g = await flow_engine.process_input(sid, "3")
        assert nxt == "CASE_CREATED"
        assert g is False
