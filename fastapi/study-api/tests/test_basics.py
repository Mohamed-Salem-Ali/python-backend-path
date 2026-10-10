"""Module 10 acceptance tests: routes, path and query parameters, response models, status codes.

Do not edit. Run from fastapi/study-api:  pytest

One test passes before you start: FastAPI serves its /docs page by itself. It is a guard, so the
docs stay on when you change the routes.
"""

from app import store


def create(client, text="one two three four five", max_words=3):
    return client.post("/summaries", json={"text": text, "max_words": max_words})


def test_health_says_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_answers_201_with_the_summary(client):
    response = create(client)
    assert response.status_code == 201
    assert response.json() == {"id": 1, "summary": "one two three...", "word_count": 5}


def test_short_text_is_not_cut_and_gets_no_dots(client):
    response = create(client, text="one two", max_words=5)
    assert response.json()["summary"] == "one two"
    assert response.json()["word_count"] == 2


def test_the_response_hides_the_owner(client):
    body = create(client).json()
    assert set(body) == {"id", "summary", "word_count"}
    assert store.SUMMARIES[1]["owner"] == "anonymous"  # the store keeps it; the reply must not


def test_a_saved_summary_can_be_fetched_and_hides_the_owner(client):
    created = create(client).json()
    response = client.get(f"/summaries/{created['id']}")
    assert response.status_code == 200
    assert response.json() == created


def test_a_missing_summary_is_a_404_with_a_detail(client):
    response = client.get("/summaries/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "summary not found"}


def test_the_id_in_the_path_must_be_a_whole_number(client):
    response = client.get("/summaries/abc")
    assert response.status_code == 422


def test_a_body_without_text_is_refused_and_names_the_field(client):
    response = client.post("/summaries", json={"max_words": 3})
    assert response.status_code == 422
    assert any(error["loc"][-1] == "text" for error in response.json()["detail"])


def test_the_list_is_in_id_order_and_can_be_paged(client):
    for _ in range(3):
        create(client)
    first = client.get("/summaries", params={"limit": 2}).json()
    assert [item["id"] for item in first] == [1, 2]
    rest = client.get("/summaries", params={"limit": 2, "offset": 2}).json()
    assert [item["id"] for item in rest] == [3]


def test_the_list_returns_at_most_20_by_default(client):
    for _ in range(25):
        create(client)
    assert len(client.get("/summaries").json()) == 20


def test_limit_must_be_between_1_and_100(client):
    assert client.get("/summaries", params={"limit": 0}).status_code == 422
    assert client.get("/summaries", params={"limit": 101}).status_code == 422


def test_delete_answers_204_with_no_body_then_404(client):
    created = create(client).json()
    response = client.delete(f"/summaries/{created['id']}")
    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/summaries/{created['id']}").status_code == 404
    assert client.delete(f"/summaries/{created['id']}").status_code == 404


def test_the_docs_page_is_served(client):
    assert client.get("/docs").status_code == 200


def test_the_openapi_spec_lists_the_routes_and_the_status_codes(client):
    spec = client.get("/openapi.json").json()
    assert "/health" in spec["paths"]
    assert "/summaries" in spec["paths"]
    assert "/summaries/{summary_id}" in spec["paths"]
    assert "201" in spec["paths"]["/summaries"]["post"]["responses"]
    assert "204" in spec["paths"]["/summaries/{summary_id}"]["delete"]["responses"]
