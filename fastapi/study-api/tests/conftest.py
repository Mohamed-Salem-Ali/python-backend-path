"""Shared fixtures for the tests. Module 10. You do not need to change this file.

Every test starts with an empty store, so one test cannot see another test's summaries.
"""

import pytest
from app import store
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def empty_store():
    store.reset()
    yield
    store.reset()


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
