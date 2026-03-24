import pytest, os; from sqlalchemy import create_engine; from sqlalchemy.orm import sessionmaker; from app.db.models import Base
@pytest.fixture(scope="session")
def db_engine():
    e = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=e); yield e; Base.metadata.drop_all(bind=e)
@pytest.fixture(scope="function")
def db_session(db_engine):
    c = db_engine.connect(); t = c.begin(); s = sessionmaker(bind=c)(); yield s; s.close(); t.rollback(); c.close()
@pytest.fixture(autouse=True)
def mock_settings(monkeypatch):
    monkeypatch.setenv("ENCRYPTION_KEY", "dmVyeS1zZWNyZXQtMzItYnl0ZS1rZXktZm9yLXRlc3Rpbmc="); monkeypatch.setenv("USE_MOCK_EPDS", "true")
