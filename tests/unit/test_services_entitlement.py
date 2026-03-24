import pytest
import os
import json
from unittest.mock import MagicMock, patch
from app.services.entitlement import get_entitlement_voice_script, get_simple_prompt

@pytest.fixture
def mock_prompts():
    return {
        "ENTITLEMENT_READ": {
            "prompt_template": "Hello {head_name}, for {month}, you get {wheat_kg}kg wheat and {rice_kg}kg rice."
        },
        "LANGUAGE_SELECT": {
            "prompt": "Please select language"
        }
    }

def test_get_simple_prompt(mock_prompts, tmp_path):
    p_dir = tmp_path / "backend" / "app" / "ivr" / "prompts"
    p_dir.mkdir(parents=True)
    with open(p_dir / "hi.json", "w", encoding="utf-8") as f:
        json.dump(mock_prompts, f)
    
    with patch("app.services.entitlement.os.path.join", side_effect=lambda *args: str(tmp_path.joinpath(*args)) if "prompts" in args else os.path.join(*args)):
        # Wait, the above patch might be tricky. Let's just mock the open() instead.
        pass

    # Simplified mock for the file read
    with patch("builtins.open", MagicMock()):
        with patch("json.load", return_value=mock_prompts):
            res = get_simple_prompt("LANGUAGE_SELECT", "hi")
            assert res == "Please select language"
            
            res = get_simple_prompt("NON_EXISTENT", "hi")
            assert res == "System error."

def test_get_entitlement_voice_script_not_found():
    with patch("app.services.entitlement.SessionLocal") as mock_session_cls, \
         patch("app.services.entitlement.epds_client") as mock_epds:
        
        mock_db = MagicMock()
        mock_session_cls.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None
        mock_epds.get_ration_card.return_value = None
        
        res = get_entitlement_voice_script("123456")
        assert res == "CARD_NOT_FOUND"

def test_get_entitlement_voice_script_found_local(mock_prompts):
    with patch("app.services.entitlement.SessionLocal") as mock_session_cls, \
         patch("app.services.entitlement.encryption_service") as mock_encryption:
        
        mock_db = MagicMock()
        mock_session_cls.return_value = mock_db
        
        mock_card = MagicMock()
        mock_card.id = 1
        mock_card.household_head_name = "encrypted_name"
        mock_db.query.return_value.filter.return_value.first.side_effect = [mock_card, MagicMock(wheat_kg=5, rice_kg=5)]
        
        mock_encryption.decrypt.return_value = "Ram"
        
        with patch("builtins.open", MagicMock()):
            with patch("json.load", return_value=mock_prompts):
                res = get_entitlement_voice_script("123456")
                assert "Ram" in res
                assert "5.0" in res

def test_get_entitlement_voice_script_found_remote(mock_prompts):
    with patch("app.services.entitlement.SessionLocal") as mock_session_cls, \
         patch("app.services.entitlement.epds_client") as mock_epds:
        
        mock_db = MagicMock()
        mock_session_cls.return_value = mock_db
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        mock_remote_card = MagicMock(head_name="Shyam")
        mock_epds.get_ration_card.return_value = mock_remote_card
        mock_epds.get_monthly_allocation.return_value = MagicMock(wheat_kg=10, rice_kg=10)
        
        with patch("builtins.open", MagicMock()):
            with patch("json.load", return_value=mock_prompts):
                res = get_entitlement_voice_script("123456")
                assert "Shyam" in res
                assert "10.0" in res
