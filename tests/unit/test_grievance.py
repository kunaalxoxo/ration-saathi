import pytest
from unittest.mock import Mock, patch
from app.services.grievance import create_grievance_case

@pytest.mark.asyncio
async def test_create_grievance_case():
    """Test creating a grievance case"""
    # Mock session data
    session_data = {
        "resolved_card_id": "test-card-id",
        "collected_data": {
            "issue_type": "wheat",
            "expected_wheat_kg": 5.0,
            "expected_rice_kg": 5.0,
            "quantity": "3.0"
        },
        "language_selected": "hi"
    }
    
    # Mock dependencies
    with patch('app.services.grievance.get_db') as mock_get_db, \
         patch('app.services.grievance.redis_client') as mock_redis, \
         patch('app.services.grievance.send_case_created_sms') as mock_sms, \
         patch('app.services.grievance.update_fps_risk_score') as mock_update_risk:
        
        # Setup mocks
        mock_db = Mock()
        mock_get_db.return_value = iter([mock_db])
        
        # Mock ration card query
        mock_ration_card = Mock()
        mock_ration_card.id = "test-card-id"
        mock_ration_card.state_code = "RJ"
        mock_ration_card.fps_code = "RJ-BA-001"
        mock_ration_card.district_code = "RJ-BA"
        mock_ration_card.block_code = "RJ-BA-001"
        mock_ration_card.phone_encrypted = "encrypted-phone"
        mock_db.query.return_value.filter.return_value.first.return_value = mock_ration_card
        
        # Mock Redis INC
        mock_redis.incr.return_value = 12345
        
        # Mock commit and refresh
        mock_db.commit.return_value = None
        mock_db.refresh.return_value = None
        
        # Call the function
        result = await create_grievance_case(session_data)
        
        # Assertions
        assert result["success"] is True
        assert "case_number" in result["data"]
        assert result["data"]["case_number"].startswith("RS-RJ-2025-")
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_sms.assert_called_once()
        mock_update_risk.assert_called_once_with("RJ-BA-001")
