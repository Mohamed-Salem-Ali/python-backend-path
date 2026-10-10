# Study API

The first stage of an AI wrapper API, built in the FastAPI track. It stores summaries and serves them over HTTP. The summary comes from a stand-in function for now. A real model call comes later, in the background.

The lessons are in [../10-basics/lesson.md](../10-basics/lesson.md) (routes) and [../10-pydantic/lesson.md](../10-pydantic/lesson.md) (validation and settings). This folder is the project you build while you work through them.

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

The limit on a summary's words comes from the environment variable `STUDY_MAX_WORDS`. It defaults to 500 when the variable is not set.

## Layout

| Path | What it is | State |
|---|---|---|
| [app/main.py](app/main.py) | The app, the router include, and the health route | TODO comments only (module 10) |
| [app/routers/summaries.py](app/routers/summaries.py) | The summaries routes: create, list, fetch and delete | TODO comments only (module 10) |
| [app/schemas.py](app/schemas.py) | The request and response models, and their validation rules | Basics ready; validation rules are TODO comments (Pydantic) |
| [app/config.py](app/config.py) | Settings read from the environment | TODO comments only (Pydantic) |
| [app/store.py](app/store.py) | In-memory storage, replaced by a database later | Ready |
| [app/summarizer.py](app/summarizer.py) | A stand-in for the AI call | Ready |
| [tests/conftest.py](tests/conftest.py) | Fixtures: a test client, and an empty store for each test | Ready |
| [tests/test_basics.py](tests/test_basics.py) | Acceptance tests for the routes (14 tests) | Ready, do not edit |
| [tests/test_validation.py](tests/test_validation.py) | Acceptance tests for the rules and the settings (11 tests) | Ready, do not edit |

## Tests

`pytest` runs both test files. Until you fill in the TODOs, most tests fail: the routes in `app/main.py` and `app/routers/summaries.py` (module 10 basics), and the rules and settings in `app/schemas.py` and `app/config.py` (Pydantic). One test passes from the start: the default of 50 words, which the basics already set.
