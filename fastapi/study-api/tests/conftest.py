"""Shared fixtures for the tests. You do not need to change this file.

The tests use their own database file. The environment variable is set before the app is imported,
because the app reads it when it starts. The migrations run once for the whole test run. Each test
then starts with an empty summaries table, so one test cannot see another test's rows.
"""

import os
import sqlite3
import tempfile
from contextlib import closing
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient

PROJECT = Path(__file__).resolve().parents[1]
TEST_DB_FILE = Path(tempfile.mkdtemp(prefix="study-api-tests-")) / "test.db"
os.environ["STUDY_DATABASE_URL"] = f"sqlite+aiosqlite:///{TEST_DB_FILE.as_posix()}"

from app.main import app  # noqa: E402  (imported after the variable above is set)


def run_sql(sql, params=()):
    """Run one SQL statement on the test database, and return the rows."""
    with closing(sqlite3.connect(TEST_DB_FILE)) as connection:
        with connection:
            return connection.execute(sql, params).fetchall()


@pytest.fixture(scope="session", autouse=True)
def migrated_database():
    command.upgrade(Config(str(PROJECT / "alembic.ini")), "head")


@pytest.fixture(autouse=True)
def empty_table(migrated_database):
    run_sql("DELETE FROM summaries")


@pytest.fixture
def client(empty_table):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def db_query():
    return run_sql
