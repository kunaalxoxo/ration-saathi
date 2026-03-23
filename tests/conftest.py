import pytest
import asyncio
from typing import Generator, AsyncGenerator
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client() -> Generator:
    with TestClient(app) as c:
        yield c

@pytest.fixture
def event_loop() -> Generator:
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()
