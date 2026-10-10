"""Module 11 (database) acceptance tests: the migrations, the models, and the data under the API.
Do not edit.

Run from fastapi/study-api:  pytest tests/test_database.py

They need the database address in the settings (TODO 12), the engine and sessions (TODO 9), the
Summary model (TODO 10), the schema change for rows (TODO 13), the routes on the database (TODO 11),
and the migrations you generate and write (lesson, sections 3 to 5).
"""

import sqlite3
from contextlib import closing
from pathlib import Path

from alembic import command
from alembic.autogenerate import compare_metadata
from alembic.config import Config
from alembic.migration import MigrationContext
from app import models  # noqa: F401  (registers the models on Base.metadata)
from app.config import get_settings
from app.database import Base
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

PROJECT = Path(__file__).resolve().parents[1]


def alembic_config():
    return Config(str(PROJECT / "alembic.ini"))


def fresh_database(tmp_path, monkeypatch):
    """Point the migrations at a new, empty database file, and return its path."""
    path = tmp_path / "migrations-test.db"
    monkeypatch.setenv("STUDY_DATABASE_URL", f"sqlite+aiosqlite:///{path.as_posix()}")
    return path


def run(path, sql, params=()):
    with closing(sqlite3.connect(path)) as connection:
        with connection:
            return connection.execute(sql, params).fetchall()


def create(client, text="one two three four", max_words=3):
    return client.post("/summaries", json={"text": text, "max_words": max_words})


# Part 1: the migrations.
def test_upgrade_creates_the_summaries_table(tmp_path, monkeypatch):
    path = fresh_database(tmp_path, monkeypatch)
    command.upgrade(alembic_config(), "head")
    columns = {row[1] for row in run(path, "PRAGMA table_info(summaries)")}
    assert {"id", "summary", "word_count", "owner", "created_at", "language"} <= columns


def test_the_migrations_match_the_models(tmp_path, monkeypatch):
    path = fresh_database(tmp_path, monkeypatch)
    command.upgrade(alembic_config(), "head")
    engine = create_engine(f"sqlite:///{path.as_posix()}")
    with engine.connect() as connection:
        context = MigrationContext.configure(connection, opts={"compare_server_default": True})
        differences = compare_metadata(context, Base.metadata)
    engine.dispose()
    assert differences == [], differences


def test_the_language_default_reaches_rows_written_before_the_column(tmp_path, monkeypatch):
    path = fresh_database(tmp_path, monkeypatch)
    command.upgrade(alembic_config(), "head")
    command.downgrade(alembic_config(), "-1")
    assert "language" not in {row[1] for row in run(path, "PRAGMA table_info(summaries)")}
    run(
        path,
        "INSERT INTO summaries (summary, word_count, owner, created_at) "
        "VALUES ('old row', 2, 'anonymous', CURRENT_TIMESTAMP)",
    )
    command.upgrade(alembic_config(), "head")
    assert run(path, "SELECT language FROM summaries") == [("en",)]


# Part 2: the settings.
def test_the_database_address_comes_from_the_environment(monkeypatch):
    monkeypatch.setenv("STUDY_DATABASE_URL", "sqlite+aiosqlite:///elsewhere.db")
    assert get_settings().database_url == "sqlite+aiosqlite:///elsewhere.db"


# Part 3: the API keeps its data in the database.
def test_a_created_summary_is_saved_in_the_database(client, db_query):
    assert create(client).status_code == 201
    assert db_query("SELECT summary, word_count, owner FROM summaries") == [
        ("one two three...", 4, "anonymous")
    ]


def test_a_new_row_gets_english_as_its_language(client, db_query):
    create(client)
    assert db_query("SELECT language FROM summaries") == [("en",)]


def test_the_database_sets_the_creation_time(client, db_query):
    create(client)
    created_at = db_query("SELECT created_at FROM summaries")[0][0]
    assert created_at


def test_data_is_kept_between_two_client_sessions(db_query):
    with TestClient(app) as first:
        summary_id = create(first).json()["id"]
    with TestClient(app) as second:
        response = second.get(f"/summaries/{summary_id}")
    assert response.status_code == 200
    assert db_query("SELECT COUNT(*) FROM summaries") == [(1,)]


def test_delete_removes_the_row(client, db_query):
    summary_id = create(client).json()["id"]
    assert client.delete(f"/summaries/{summary_id}").status_code == 204
    assert db_query("SELECT COUNT(*) FROM summaries") == [(0,)]


def test_the_list_reads_rows_written_outside_the_api(client, db_query):
    db_query(
        "INSERT INTO summaries (summary, word_count, owner, created_at) "
        "VALUES ('written directly', 2, 'anonymous', CURRENT_TIMESTAMP)"
    )
    assert [item["summary"] for item in client.get("/summaries").json()] == ["written directly"]


def test_a_row_written_outside_the_api_can_be_fetched_by_id(client, db_query):
    db_query(
        "INSERT INTO summaries (summary, word_count, owner, created_at) "
        "VALUES ('written directly', 2, 'anonymous', CURRENT_TIMESTAMP)"
    )
    row_id = db_query("SELECT id FROM summaries")[0][0]
    response = client.get(f"/summaries/{row_id}")
    assert response.status_code == 200
    assert response.json()["summary"] == "written directly"
