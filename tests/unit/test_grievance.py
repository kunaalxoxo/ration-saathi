import pytest
import uuid
from datetime import date
from unittest.mock import Mock, patch
from app.services.grievance import create_grievance_case, GrievanceCreate
from app.db.models import GrievanceCase

@pytest.mark.asyncio
async def test_create_grievance_case():
    """Test creating a grievance case with proper mocks."""
    # Input data
    data = GrievanceCreate(
        ration_card_id=uuid.uuid4(),
        reporter_type="citizen",
        issue_type="wheat",
        reported_month_year=date(2025, 3, 1),
        expected_wheat_kg=5.0,
        expected_rice_kg=5.0,
        received_wheat_kg=2.0,
        received_rice_kg=5.0,
        fps_code="RJ-BA-001",
        district_code="RJ-BA",
        block_code="RJ-BA-001",
        reporter_phone="9988776655"
    )

    # Mocks
    mock_db = MagicMock()
    mock_redis = MagicMock()
    mock_redis.incr.return_value = 123
    
    with patch('app.services.grievance.SessionLocal', return_value=mock_db), \
         patch('app.services.grievance.Redis', return_value=mock_redis), \
         patch('app.worker.send_sms_task.delay') as mock_sms, \
         patch('app.worker.update_fps_risk_score_task.delay') as mock_risk:
        
        # Call the function
        result = await create_grievance_case(data)
        
        # Assertions
        assert isinstance(result, GrievanceCase)
        assert result.case_number.startswith("RS-RJ-2026-00123")
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()
        mock_db.refresh.assert_called_once()
        mock_sms.assert_called_once()
        mock_risk.assert_called_once_with("RJ-BA-001")

from unittest.mock import MagicMock
