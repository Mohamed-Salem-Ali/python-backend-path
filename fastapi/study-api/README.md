# Study API

The first stage of an AI wrapper API, built in the FastAPI track. It stores summaries and serves them over HTTP. The summary comes from a stand-in function for now. A real model call comes later, in the background.

The lessons are in [../10-basics/lesson.md](../10-basics/lesson.md). This folder is the project you build while you work through them.

## Setup and run

From this folder:

```bash
pip install -r requirements.txt
```

Run the tests:

```bash
pytest
```

Start the server, then open `http://127.0.0.1:8000/docs`:

```bash
uvicorn app.main:app --reload
```

## Layout

| Path | What it is | State |
|---|---|---|
| [app/main.py](app/main.py) | The app, the router include, and the health route | TODO comments only (module 10) |
| [app/routers/summaries.py](app/routers/summaries.py) | The summaries routes: create, list, fetch and delete | TODO comments only (module 10) |
| [app/schemas.py](app/schemas.py) | The request and response models | Ready |
| [app/store.py](app/store.py) | In-memory storage, replaced by a database later | Ready |
| [app/summarizer.py](app/summarizer.py) | A stand-in for the AI call | Ready |
| [tests/conftest.py](tests/conftest.py) | Fixtures: a test client, and an empty store for each test | Ready |
| [tests/test_basics.py](tests/test_basics.py) | Acceptance tests for module 10 (14 tests) | Ready, do not edit |

## Tests

`pytest` runs `tests/test_basics.py`. Most tests fail until you fill in the TODOs in `app/main.py` and `app/routers/summaries.py`. One test, the docs page, passes from the start.
