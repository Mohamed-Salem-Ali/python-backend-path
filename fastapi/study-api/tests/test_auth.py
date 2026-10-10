"""Module 11 (auth) acceptance tests: passwords, tokens, protected routes and who owns a summary.
Do not edit.

Run from fastapi/study-api:  pytest tests/test_auth.py

They need the settings (TODO 14), the User model (TODO 15), the password and token functions
(TODO 16), the request and response shapes (TODO 17), the dependencies (TODO 18), the auth and
me routes (TODO 19 and 20), the owner on create (TODO 21) and the routers in the app (TODO 22).
The users table comes from a migration you generate (lesson, section 4).
"""

from datetime import UTC, datetime, timedelta

import jwt
import pytest
from app.config import get_settings
from app.dependencies import get_current_user
from app.main import app
from app.models import User
from app.security import create_access_token, verify_password
from pydantic import ValidationError

PASSWORD = "correct horse battery"


@pytest.fixture(autouse=True)
def empty_users(db_query):
    db_query("DELETE FROM users")


def register(client, username="ada", password=PASSWORD):
    return client.post("/auth/register", json={"username": username, "password": password})


def login(client, username="ada", password=PASSWORD):
    return client.post("/auth/token", data={"username": username, "password": password})


def signed_up_headers(client, username="ada"):
    """Register a user, log in, and return the header that carries the token."""
    assert register(client, username).status_code == 201
    token = login(client, username).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def create_summary(client, headers=None):
    body = {"text": "one two three four", "max_words": 3}
    return client.post("/summaries", json=body, headers=headers or {})


# Part 1: the settings.
def test_the_secret_key_is_required(monkeypatch):
    monkeypatch.delenv("STUDY_SECRET_KEY")
    with pytest.raises(ValidationError):
        get_settings()


def test_a_short_secret_key_is_refused(monkeypatch):
    monkeypatch.setenv("STUDY_SECRET_KEY", "too-short")
    with pytest.raises(ValidationError):
        get_settings()


def test_the_token_lifetime_comes_from_the_environment(monkeypatch):
    monkeypatch.setenv("STUDY_ACCESS_TOKEN_MINUTES", "5")
    assert get_settings().access_token_minutes == 5


def test_a_token_expires_after_the_configured_minutes(monkeypatch):
    monkeypatch.setenv("STUDY_ACCESS_TOKEN_MINUTES", "5")
    payload = jwt.decode(create_access_token(1), get_settings().secret_key, algorithms=["HS256"])
    lifetime = payload["exp"] - datetime.now(UTC).timestamp()
    assert 4 * 60 < lifetime <= 5 * 60


# Part 2: registering.
def test_register_answers_201_with_the_user_and_no_password(client):
    response = register(client)
    assert response.status_code == 201
    assert response.json() == {"id": 1, "username": "ada"}


def test_the_password_is_stored_as_a_hash(client, db_query):
    register(client)
    stored = db_query("SELECT password_hash FROM users WHERE username = ?", ("ada",))[0][0]
    assert PASSWORD not in stored
    assert verify_password(PASSWORD, stored)


def test_a_taken_username_is_a_409(client):
    register(client)
    response = register(client)
    assert response.status_code == 409
    assert response.json() == {"detail": "username already taken"}


def test_a_short_password_is_refused(client):
    assert register(client, password="short").status_code == 422


# Part 3: logging in.
def test_login_gives_a_bearer_token(client):
    register(client)
    response = login(client)
    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"
    assert isinstance(response.json()["access_token"], str)


def test_a_wrong_password_and_an_unknown_user_get_the_same_401(client):
    register(client)
    for response in (login(client, password="wrong password here"), login(client, "nobody")):
        assert response.status_code == 401
        assert response.json() == {"detail": "incorrect username or password"}
        assert response.headers["WWW-Authenticate"] == "Bearer"


# Part 4: the protected route, GET /me.
def test_me_without_a_token_is_a_401(client):
    response = client.get("/me")
    assert response.status_code == 401
    assert response.headers["WWW-Authenticate"] == "Bearer"


def test_me_with_a_valid_token_returns_the_user(client):
    response = client.get("/me", headers=signed_up_headers(client))
    assert response.status_code == 200
    assert response.json() == {"id": 1, "username": "ada"}


def test_a_token_signed_with_another_key_is_a_401(client):
    signed_up_headers(client)
    forged = jwt.encode({"sub": "1"}, "x" * 40, algorithm="HS256")
    response = client.get("/me", headers={"Authorization": f"Bearer {forged}"})
    assert response.status_code == 401


def test_an_expired_token_is_a_401(client):
    signed_up_headers(client)
    expired = datetime.now(UTC) - timedelta(minutes=1)
    token = jwt.encode({"sub": "1", "exp": expired}, get_settings().secret_key, algorithm="HS256")
    assert client.get("/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_a_token_whose_subject_is_not_a_number_is_a_401(client):
    signed_up_headers(client)
    token = jwt.encode({"sub": "ada"}, get_settings().secret_key, algorithm="HS256")
    assert client.get("/me", headers={"Authorization": f"Bearer {token}"}).status_code == 401


def test_a_token_for_a_deleted_user_is_a_401(client, db_query):
    headers = signed_up_headers(client)
    db_query("DELETE FROM users")
    assert client.get("/me", headers=headers).status_code == 401


# Part 5: who owns a summary.
def test_a_summary_created_with_a_token_belongs_to_its_user(client, db_query):
    response = create_summary(client, headers=signed_up_headers(client))
    assert response.status_code == 201
    assert set(response.json()) == {"id", "summary", "word_count"}
    assert db_query("SELECT owner FROM summaries") == [("ada",)]


def test_a_bad_token_on_an_open_route_is_refused_and_saves_nothing(client, db_query):
    response = create_summary(client, headers={"Authorization": "Bearer not-a-token"})
    assert response.status_code == 401
    assert db_query("SELECT COUNT(*) FROM summaries") == [(0,)]


def test_my_summaries_lists_only_the_users_own(client):
    ada = signed_up_headers(client, "ada")
    bob = signed_up_headers(client, "bob")
    first = create_summary(client, headers=ada).json()["id"]
    second = create_summary(client, headers=ada).json()["id"]
    create_summary(client, headers=bob)
    create_summary(client)  # no token: owned by "anonymous"
    response = client.get("/me/summaries", headers=ada)
    assert response.status_code == 200
    assert [item["id"] for item in response.json()] == [first, second]


def test_my_summaries_needs_a_token(client):
    assert client.get("/me/summaries").status_code == 401


# Part 6: the docs, and replacing a dependency in a test.
def test_the_docs_mark_the_protected_routes_and_not_the_health_route(client):
    spec = client.get("/openapi.json").json()
    assert "security" in spec["paths"]["/me"]["get"]
    assert "security" not in spec["paths"]["/health"]["get"]


def test_a_dependency_override_replaces_the_login_in_a_test(client):
    fake_user = User(id=7, username="tester")
    app.dependency_overrides[get_current_user] = lambda: fake_user
    try:
        response = client.get("/me")
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 200
    assert response.json() == {"id": 7, "username": "tester"}
