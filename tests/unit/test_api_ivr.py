import pytest
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import MagicMock, patch, AsyncMock

client = TestClient(app)

@pytest.fixture
def mock_flow():
    with patch("app.api.ivr_webhook.flow_engine") as mock:
        mock.process_input = AsyncMock()
        yield mock

def test_ivr_inbound(mock_flow):
    mock_flow.process_input.return_value = ("LANGUAGE_SELECT", "Welcome", True)
    
    response = client.post("/ivr/inbound", data={"CallSid": "test_sid"})
    assert response.status_code == 200
    assert "Welcome" in response.text
    assert "Gather" in response.text

def test_ivr_gather(mock_flow):
    mock_flow.process_input.return_value = ("RATION_CARD_INPUT", "Enter card", True)
    
    response = client.post("/ivr/gather", data={"CallSid": "test_sid", "Digits": "1"})
    assert response.status_code == 200
    assert "Enter card" in response.text
    
def test_ivr_gather_completed(mock_flow):
    mock_flow.process_input.return_value = ("CALL_COMPLETED", "Goodbye", False)
    
    response = client.post("/ivr/gather", data={"CallSid": "test_sid", "Digits": "123456"})
    assert response.status_code == 200
    assert "Goodbye" in response.text
    assert "Hangup" in response.text
