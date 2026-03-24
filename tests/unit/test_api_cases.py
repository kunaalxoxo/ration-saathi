import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db
from unittest.mock import MagicMock

client = TestClient(app)

@pytest.fixture
def mock_db():
    db = MagicMock()
    yield db

def test_get_case_status_not_found(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.get("/cases/RS-RJ-2025-00001")
    assert response.status_code == 404
    assert response.json()["detail"] == "Case not found"
    
    app.dependency_overrides.clear()

def test_get_case_status_success(mock_db):
    mock_case = MagicMock()
    mock_case.case_number = "RS-RJ-2025-00001"
    mock_case.status = "open"
    mock_case.created_at.isoformat.return_value = "2025-03-01T10:00:00"
    mock_case.issue_type = "wheat"
    
    mock_db.query.return_value.filter.return_value.first.return_value = mock_case
    app.dependency_overrides[get_db] = lambda: mock_db
    
    response = client.get("/cases/RS-RJ-2025-00001")
    assert response.status_code == 200
    assert response.json()["status"] == "open"
    
    app.dependency_overrides.clear()
