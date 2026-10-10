"""Module 12 (background work) acceptance tests: queueing a job, the job itself, async tests and
dependency overrides. Do not edit.

Run from fastapi/study-api:  pytest tests/test_background.py

They need the foreign-key setting (TODO 23), the Flashcard model (TODO 24), the response shapes
(TODO 25), the job and its dependency (TODO 26), the routes (TODO 27), and the migration you
generate (lesson, section 4). The stand-in maker in app/flashcards.py is already written.
"""

import asyncio
import threading

import httpx2
import pytest
from app.main import app
from app.services import get_flashcard_maker, write_flashcards

TEXT = "one two three. four five six"
ONE = "Recall the sentence that starts with 'one'"
FOUR = "Recall the sentence that starts with 'four'"


@pytest.fixture(autouse=True)
def empty_flashcards(db_query):
    db_query("DELETE FROM flashcards")


def create(client, text=TEXT):
    return client.post("/summaries", json={"text": text, "max_words": 50}).json()["id"]


def queue(client, summary_id):
    return client.post(f"/summaries/{summary_id}/flashcards")


def cards(client, summary_id):
    listed = client.get(f"/summaries/{summary_id}/flashcards").json()
    return [(card["front"], card["back"]) for card in listed]


def insert_summary(db_query, text="one two three"):
    db_query(
        "INSERT INTO summaries (summary, word_count, owner, created_at) "
        "VALUES (?, 3, 'anonymous', CURRENT_TIMESTAMP)",
        (text,),
    )
    return db_query("SELECT MAX(id) FROM summaries")[0][0]


def async_client():
    return httpx2.AsyncClient(transport=httpx2.ASGITransport(app=app), base_url="http://test")


# Part 1: queueing from the route. The TestClient waits for the background job, so the cards
# exist by the time the call returns. In production the job runs after the response is sent.
def test_queueing_answers_202_with_the_summary_id(client):
    summary_id = create(client)
    response = queue(client, summary_id)
    assert response.status_code == 202
    assert response.json() == {"status": "queued", "summary_id": summary_id}


def test_queueing_for_a_missing_summary_is_a_404(client):
    response = queue(client, 999)
    assert response.status_code == 404
    assert response.json() == {"detail": "summary not found"}


def test_the_cards_are_there_once_the_call_returns(client):
    summary_id = create(client)
    queue(client, summary_id)
    assert cards(client, summary_id) == [(ONE, "one two three"), (FOUR, "four five six")]


def test_a_summary_with_no_cards_yet_has_an_empty_list(client):
    assert client.get(f"/summaries/{create(client)}/flashcards").json() == []


def test_each_summary_only_lists_its_own_cards(client):
    first = create(client)
    second = create(client, text="seven eight nine")
    queue(client, first)
    assert cards(client, second) == []


def test_a_second_queue_replaces_the_cards(client):
    summary_id = create(client)
    queue(client, summary_id)
    queue(client, summary_id)
    assert len(cards(client, summary_id)) == 2


def test_the_cards_of_a_missing_summary_are_a_404(client):
    response = client.get("/summaries/999/flashcards")
    assert response.status_code == 404
    assert response.json() == {"detail": "summary not found"}


# Part 2: the job itself. Tests call it directly, with anyio's pytest plugin for async tests.
@pytest.mark.anyio
async def test_the_job_saves_the_cards_its_maker_returns(db_query):
    summary_id = insert_summary(db_query)
    await write_flashcards(summary_id, lambda text: [("Q", "A")])
    assert db_query("SELECT front, back FROM flashcards") == [("Q", "A")]


@pytest.mark.anyio
async def test_the_job_keeps_the_old_cards_when_the_maker_fails(db_query, caplog):
    summary_id = insert_summary(db_query)
    await write_flashcards(summary_id, lambda text: [("Q", "A")])

    def broken(text):
        raise RuntimeError("the model is down")

    await write_flashcards(summary_id, broken)
    assert db_query("SELECT front FROM flashcards") == [("Q",)]
    assert "could not make flashcards" in caplog.text


@pytest.mark.anyio
async def test_the_job_does_nothing_for_a_missing_summary(db_query):
    await write_flashcards(999, lambda text: [("Q", "A")])
    assert db_query("SELECT COUNT(*) FROM flashcards") == [(0,)]


@pytest.mark.anyio
async def test_the_maker_runs_in_a_worker_thread_not_on_the_event_loop(db_query):
    summary_id = insert_summary(db_query)
    threads = []

    def record(text):
        threads.append(threading.current_thread())
        return []

    await write_flashcards(summary_id, record)
    assert threads and threads[0] is not threading.main_thread()


# Part 3: async tests. The async client calls the app in the test's own event loop.
@pytest.mark.anyio
async def test_the_async_client_creates_queues_and_reads(db_query):
    async with async_client() as client:
        created = await client.post("/summaries", json={"text": TEXT, "max_words": 50})
        summary_id = created.json()["id"]
        queued = await client.post(f"/summaries/{summary_id}/flashcards")
        listed = await client.get(f"/summaries/{summary_id}/flashcards")
    assert queued.status_code == 202
    assert [card["back"] for card in listed.json()] == ["one two three", "four five six"]


@pytest.mark.anyio
async def test_five_reads_at_the_same_time_all_succeed(db_query):
    summary_id = insert_summary(db_query)
    async with async_client() as client:
        responses = await asyncio.gather(
            *(client.get(f"/summaries/{summary_id}/flashcards") for _ in range(5))
        )
    assert [response.status_code for response in responses] == [200] * 5


# Part 4: dependency overrides replace the maker, so a test decides what the job receives.
def test_the_route_gives_the_job_the_maker_from_the_dependency(client):
    received = []

    def fake(text):
        received.append(text)
        return [("Q", "A")]

    app.dependency_overrides[get_flashcard_maker] = lambda: fake
    try:
        summary_id = create(client)
        queue(client, summary_id)
    finally:
        app.dependency_overrides.clear()
    assert received == [TEXT]
    assert cards(client, summary_id) == [("Q", "A")]


def test_a_failing_maker_still_answers_202_and_saves_nothing(client):
    def broken(text):
        raise RuntimeError("the model is down")

    app.dependency_overrides[get_flashcard_maker] = lambda: broken
    try:
        summary_id = create(client)
        response = queue(client, summary_id)
    finally:
        app.dependency_overrides.clear()
    assert response.status_code == 202
    assert cards(client, summary_id) == []


# Part 5: the database keeps the cards in step with their summary.
def test_deleting_a_summary_deletes_its_cards(client, db_query):
    summary_id = create(client)
    assert queue(client, summary_id).status_code == 202
    assert db_query("SELECT COUNT(*) FROM flashcards") == [(2,)]
    assert client.delete(f"/summaries/{summary_id}").status_code == 204
    assert db_query("SELECT COUNT(*) FROM flashcards") == [(0,)]


def test_the_cards_reference_the_summary_with_a_cascade(db_query):
    rows = db_query("SELECT \"table\", on_delete FROM pragma_foreign_key_list('flashcards')")
    assert ("summaries", "CASCADE") in rows


# Part 6: the docs.
def test_the_docs_show_the_queue_route_answers_202(client):
    spec = client.get("/openapi.json").json()
    assert "202" in spec["paths"]["/summaries/{summary_id}/flashcards"]["post"]["responses"]
