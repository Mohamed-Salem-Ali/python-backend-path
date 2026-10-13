"""Module 13 (a real model and rate limits) acceptance tests. Do not edit.

Run from fastapi/study-api:  pytest tests/test_ai.py

They need the model settings (TODO 30), the model client in app/ai.py (TODO 31), the two
dependencies that choose a maker (TODO 32), the create route on the summarizer dependency
(TODO 33), the rate limiter in app/ratelimit.py (TODO 34), and the limits on the routes (TODO 35).

No test calls a real model. The client tests give httpx2 a fake transport that answers like the
Gemini API, and the route tests replace the summarizer with a dependency override.
"""

import json
import threading

import httpx2
import pytest
from app.ai import (
    ModelError,
    fit_words,
    gemini_flashcard_maker,
    gemini_summarizer,
    generate,
    get_summarizer,
)
from app.config import get_settings
from app.flashcards import make_flashcards
from app.main import app
from app.ratelimit import RateLimiter, get_rate_limiter
from app.services import get_flashcard_maker
from app.summarizer import summarize
from pydantic import ValidationError

KEY = "fake-key-for-tests"
PASSWORD = "correct horse battery"


@pytest.fixture(autouse=True)
def empty_users(db_query):
    db_query("DELETE FROM users")


@pytest.fixture
def gemini_settings(monkeypatch):
    monkeypatch.setenv("STUDY_AI_PROVIDER", "gemini")
    monkeypatch.setenv("STUDY_AI_API_KEY", KEY)
    return get_settings()


def answer(*parts):
    """A response body shaped like the Gemini API's, with the given parts."""
    return {"candidates": [{"content": {"parts": list(parts)}}]}


def fake_model(reply, seen=None):
    """A transport that records each request in `seen` and answers with `reply`."""

    def handle(request):
        if seen is not None:
            seen.append(request)
        return reply(request) if callable(reply) else httpx2.Response(200, json=reply)

    return httpx2.MockTransport(handle)


def override(dependency, value):
    app.dependency_overrides[dependency] = lambda: value


@pytest.fixture(autouse=True)
def clear_overrides():
    yield
    app.dependency_overrides.clear()


def create(client, text="one two three four five", max_words=3, headers=None):
    body = {"text": text, "max_words": max_words}
    return client.post("/summaries", json=body, headers=headers or {})


def login(client, username):
    return client.post("/auth/token", data={"username": username, "password": PASSWORD})


def headers_for(client, username):
    assert (
        client.post("/auth/register", json={"username": username, "password": PASSWORD}).status_code
        == 201
    )
    return {"Authorization": f"Bearer {login(client, username).json()['access_token']}"}


def limiter(limit, start=0.0):
    """A limiter with a clock the test moves by hand: clock[0] is the current time in seconds."""
    clock = [start]
    return RateLimiter(limit, window_seconds=60, clock=lambda: clock[0]), clock


# Part 1: the settings.
def test_the_model_settings_have_safe_defaults(monkeypatch):
    monkeypatch.delenv("STUDY_RATE_LIMIT_PER_MINUTE")
    settings = get_settings()
    assert settings.ai_provider == "stub"
    assert settings.ai_api_key is None
    assert settings.ai_model == "gemini-3.5-flash-lite"
    assert settings.rate_limit_per_minute == 10


def test_the_gemini_provider_without_a_key_is_refused(monkeypatch):
    monkeypatch.setenv("STUDY_AI_PROVIDER", "gemini")
    with pytest.raises(ValidationError, match="STUDY_AI_API_KEY"):
        get_settings()


def test_the_key_is_hidden_when_the_settings_are_printed(gemini_settings):
    assert KEY not in repr(gemini_settings)
    assert KEY not in str(gemini_settings.model_dump())
    assert gemini_settings.ai_api_key.get_secret_value() == KEY


def test_the_rate_limit_cannot_be_negative(monkeypatch):
    monkeypatch.setenv("STUDY_RATE_LIMIT_PER_MINUTE", "-1")
    with pytest.raises(ValidationError):
        get_settings()


# Part 2: the model client.
def test_generate_posts_the_prompt_to_the_model(gemini_settings):
    seen = []
    generate("Say hi", gemini_settings, transport=fake_model(answer({"text": "hi"}), seen))
    request = seen[0]
    assert request.method == "POST"
    assert request.url.path.endswith("/models/gemini-3.5-flash-lite:generateContent")
    body = json.loads(request.content)
    assert body["contents"][0]["parts"][0]["text"] == "Say hi"


def test_the_key_goes_in_a_header_not_in_the_address(gemini_settings):
    seen = []
    generate("Say hi", gemini_settings, transport=fake_model(answer({"text": "hi"}), seen))
    assert seen[0].headers["x-goog-api-key"] == KEY
    assert KEY not in str(seen[0].url)


def test_generate_joins_the_text_parts_and_skips_the_thoughts(gemini_settings):
    reply = answer({"text": "planning...", "thought": True}, {"text": "Hello"}, {"text": " there"})
    assert generate("Say hi", gemini_settings, transport=fake_model(reply)) == "Hello there"


def test_a_server_error_becomes_a_model_error_even_if_its_body_looks_fine(gemini_settings):
    # The status code decides, not the body: a proxy can send an error with any body.
    reply = answer({"text": "hi"})
    transport = fake_model(lambda request: httpx2.Response(503, json=reply))
    with pytest.raises(ModelError):
        generate("Say hi", gemini_settings, transport=transport)


def test_a_timeout_becomes_a_model_error(gemini_settings):
    def slow(request):
        raise httpx2.ReadTimeout("the model took too long", request=request)

    with pytest.raises(ModelError):
        generate("Say hi", gemini_settings, transport=fake_model(slow))


def test_an_answer_with_no_text_is_a_model_error(gemini_settings):
    for reply in ({"candidates": []}, answer({"text": "  "}), {"unexpected": True}):
        with pytest.raises(ModelError):
            generate("Say hi", gemini_settings, transport=fake_model(reply))


def test_fit_words_cuts_a_long_text_to_the_limit():
    assert fit_words("one two three four", 2) == "one two..."
    assert fit_words("one two", 2) == "one two"


def test_the_summarizer_puts_the_text_and_the_word_limit_in_the_prompt(gemini_settings):
    seen = []
    summarizer = gemini_summarizer(gemini_settings, fake_model(answer({"text": "short"}), seen))
    assert summarizer("A long text about savings circles.", 12) == "short"
    prompt = json.loads(seen[0].content)["contents"][0]["parts"][0]["text"]
    assert "A long text about savings circles." in prompt
    assert "12" in prompt


def test_the_flashcard_maker_asks_for_json_and_returns_pairs(gemini_settings):
    seen = []
    cards = json.dumps([{"front": "What is a gameya?", "back": "A savings circle"}])
    maker = gemini_flashcard_maker(gemini_settings, fake_model(answer({"text": cards}), seen))
    assert maker("Some text") == [("What is a gameya?", "A savings circle")]
    config = json.loads(seen[0].content)["generationConfig"]
    assert config["responseMimeType"] == "application/json"


def test_flashcards_that_are_not_the_expected_json_are_a_model_error(gemini_settings):
    for text in ("not json at all", json.dumps([{"question": "no front or back"}])):
        maker = gemini_flashcard_maker(gemini_settings, fake_model(answer({"text": text})))
        with pytest.raises(ModelError):
            maker("Some text")


# Part 3: the settings choose the maker.
def test_the_stub_provider_uses_the_stand_ins():
    assert get_summarizer() is summarize
    assert get_flashcard_maker() is make_flashcards


def test_the_gemini_provider_uses_the_model(gemini_settings):
    summarizer, maker = get_summarizer(), get_flashcard_maker()
    assert callable(summarizer) and summarizer is not summarize
    assert callable(maker) and maker is not make_flashcards


# Part 4: the create route uses the summarizer it is given.
def test_create_saves_what_the_summarizer_returns(client):
    received = []

    def fake(text, max_words):
        received.append((text, max_words))
        return "a model summary"

    override(get_summarizer, fake)
    response = create(client)
    assert response.status_code == 201
    assert response.json()["summary"] == "a model summary"
    assert received == [("one two three four five", 3)]


def test_a_long_model_answer_is_cut_to_max_words(client):
    override(get_summarizer, lambda text, max_words: "far too many words from the model")
    assert create(client, max_words=3).json()["summary"] == "far too many..."


def test_a_model_failure_is_a_502_and_saves_nothing(client, db_query):
    def broken(text, max_words):
        raise ModelError("the model is down")

    override(get_summarizer, broken)
    response = create(client)
    assert response.status_code == 502
    assert response.json() == {"detail": "the model is unavailable"}
    assert db_query("SELECT COUNT(*) FROM summaries") == [(0,)]


@pytest.mark.anyio
async def test_the_summarizer_runs_in_a_worker_thread_not_on_the_event_loop(db_query):
    # The async client runs the app on this test's event loop, in this thread. A summarizer
    # called straight from the route would run here too, and block every other request.
    threads = []

    def record(text, max_words):
        threads.append(threading.current_thread())
        return "ok"

    override(get_summarizer, record)
    transport = httpx2.ASGITransport(app=app)
    async with httpx2.AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/summaries", json={"text": "one two", "max_words": 5})
    assert response.status_code == 201
    assert threads and threads[0] is not threading.current_thread()


# Part 5: the limiter on its own.
def test_the_limiter_allows_the_limit_then_says_how_long_to_wait():
    limit, clock = limiter(2)
    assert limit.hit("ada") is None
    clock[0] = 10
    assert limit.hit("ada") is None
    clock[0] = 15
    assert limit.hit("ada") == pytest.approx(45)


def test_the_limiter_forgets_hits_older_than_the_window():
    limit, clock = limiter(1)
    assert limit.hit("ada") is None
    clock[0] = 60
    assert limit.hit("ada") is None


def test_each_key_has_its_own_count():
    limit, _ = limiter(1)
    assert limit.hit("ada") is None
    assert limit.hit("grace") is None
    assert limit.hit("ada") is not None


def test_a_limit_of_zero_never_blocks():
    limit, _ = limiter(0)
    assert all(limit.hit("ada") is None for _ in range(100))


# Part 6: the limits on the routes.
def test_the_third_create_in_a_minute_is_a_429_with_retry_after(client):
    limit, clock = limiter(2)
    override(get_rate_limiter, limit)
    assert [create(client).status_code for _ in range(2)] == [201, 201]
    clock[0] = 20
    response = create(client)
    assert response.status_code == 429
    assert response.json() == {"detail": "too many requests"}
    assert response.headers["Retry-After"] == "40"


def test_each_signed_in_user_has_their_own_budget(client):
    limit, _ = limiter(2)
    override(get_rate_limiter, limit)
    ada, grace = headers_for(client, "ada"), headers_for(client, "grace")
    assert [create(client, headers=ada).status_code for _ in range(3)] == [201, 201, 429]
    assert create(client, headers=grace).status_code == 201


def test_login_attempts_are_limited_even_with_the_right_password(client):
    limit, _ = limiter(2)
    override(get_rate_limiter, limit)
    client.post("/auth/register", json={"username": "ada", "password": PASSWORD})
    statuses = [login(client, "ada").status_code for _ in range(3)]
    assert statuses == [200, 200, 429]


def test_login_and_create_have_separate_budgets(client):
    limit, _ = limiter(1)
    override(get_rate_limiter, limit)
    client.post("/auth/register", json={"username": "ada", "password": PASSWORD})
    assert login(client, "ada").status_code == 200
    assert create(client).status_code == 201


def test_the_docs_list_429_and_502_for_create(client):
    responses = client.get("/openapi.json").json()["paths"]["/summaries"]["post"]["responses"]
    assert {"429", "502"} <= set(responses)
