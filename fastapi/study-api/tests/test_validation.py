"""Module 10 (Pydantic) acceptance tests: validation rules, error messages, settings from the
environment, and the limits shown in the docs. Do not edit.

Run from fastapi/study-api:  pytest tests/test_validation.py

They need the rules on SummaryIn (TODO 8), the Settings class (TODO 7), and the summaries routes
from the basics (module 10, TODOs 1 to 4). One test passes from the start: the default of 50 words
was already in the basics, so it guards that default while you add the rules.
"""

import pytest
from app.config import get_settings
from app.schemas import SummaryIn
from pydantic import ValidationError


def create(client, **body):
    return client.post("/summaries", json=body)


def words(count):
    return " ".join(f"w{i}" for i in range(count))


def test_blank_text_is_refused(client):
    assert create(client, text="   ", max_words=3).status_code == 422


def test_the_error_names_the_field_and_says_the_text_must_not_be_blank(client):
    detail = create(client, text="   ").json()["detail"]
    assert detail[0]["loc"] == ["body", "text"]
    assert "text must not be blank" in detail[0]["msg"]


def test_text_is_trimmed_when_the_schema_reads_it():
    # The summary splits on spaces, so the reply cannot show the trim. Check the schema itself.
    assert SummaryIn(text="  one two three four  ").text == "one two three four"


def test_max_words_defaults_to_50(client):
    summary = create(client, text=words(60)).json()["summary"]
    assert summary.endswith("...")
    assert len(summary.removesuffix("...").split()) == 50


def test_max_words_must_be_at_least_one(client):
    assert create(client, text="one two", max_words=0).status_code == 422


def test_max_words_cannot_go_past_the_limit(client):
    assert create(client, text=words(600), max_words=501).status_code == 422
    assert create(client, text=words(600), max_words=500).status_code == 201


def test_an_unknown_field_is_refused_so_clients_cannot_set_the_owner(client):
    response = create(client, text="one two", owner="admin")
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "owner"]


def test_the_limit_comes_from_the_environment(monkeypatch):
    monkeypatch.setenv("STUDY_MAX_WORDS", "7")
    assert get_settings().max_words == 7


def test_without_the_environment_the_limit_is_500(monkeypatch):
    monkeypatch.delenv("STUDY_MAX_WORDS", raising=False)
    assert get_settings().max_words == 500


def test_a_non_number_in_the_environment_is_refused(monkeypatch):
    monkeypatch.setenv("STUDY_MAX_WORDS", "lots")
    with pytest.raises(ValidationError):
        get_settings()


def test_the_docs_show_the_limits_of_max_words(client):
    spec = client.get("/openapi.json").json()
    max_words = spec["components"]["schemas"]["SummaryIn"]["properties"]["max_words"]
    assert max_words["minimum"] == 1
    assert max_words["maximum"] == 500
