# Study API

The first stage of an AI wrapper API, built in the FastAPI track. It stores summaries in a database and serves them over HTTP. The summary comes from a stand-in function for now. A real model call comes later, in the background.

The lessons are in [../10-basics/lesson.md](../10-basics/lesson.md) (routes), [../10-pydantic/lesson.md](../10-pydantic/lesson.md) (validation and settings) and [../11-database/lesson.md](../11-database/lesson.md) (the database and migrations). This folder is the project you build while you work through them.

## Setup and run

From this folder:

```bash
pip install -r requirements.txt
```

Create the database tables. This writes `study.db` in this folder, and the address comes from `STUDY_DATABASE_URL`, which defaults to `sqlite+aiosqlite:///./study.db`:

```bash
alembic upgrade head
```

Run the tests. They use their own database file, so they do not touch `study.db`:

```bash
pytest
```

Start the server, then open `http://127.0.0.1:8000/docs`:

```bash
uvicorn app.main:app --reload
```

Two settings come from the environment. `STUDY_MAX_WORDS` is the limit on a summary's words, and it defaults to 500. `STUDY_DATABASE_URL` is the database address, and it defaults to the SQLite file above.

## Layout

| Path | What it is | State |
|---|---|---|
| [app/main.py](app/main.py) | The app, the router include, and the health route | TODO comments only (module 10) |
| [app/routers/summaries.py](app/routers/summaries.py) | The summaries routes: create, list, fetch and delete | TODO comments only (module 10, then the database in module 11) |
| [app/schemas.py](app/schemas.py) | The request and response models, and their validation rules | Basics ready; validation and row reading are TODO comments (Pydantic, database) |
| [app/config.py](app/config.py) | Settings read from the environment, including the database address | TODO comments only (Pydantic, database) |
| [app/database.py](app/database.py) | The async engine, the session for each request, and the base class | TODO comments only (module 11) |
| [app/models.py](app/models.py) | The `Summary` table | TODO comments only (module 11) |
| [app/store.py](app/store.py) | The first in-memory storage. Delete it once no route uses it | Ready until module 11 replaces it |
| [app/summarizer.py](app/summarizer.py) | A stand-in for the AI call | Ready |
| [alembic.ini](alembic.ini), [migrations/env.py](migrations/env.py) | Alembic's settings and the migration environment | Ready |
| [migrations/versions/](migrations/versions/) | The migration files. You generate them (module 11, lesson sections 4 and 5) | Empty until you generate them |
| [tests/conftest.py](tests/conftest.py) | Fixtures: a migrated test database, an empty table for each test, and a test client | Ready |
| [tests/test_basics.py](tests/test_basics.py) | Acceptance tests for the routes (14 tests) | Ready, do not edit |
| [tests/test_validation.py](tests/test_validation.py) | Acceptance tests for the rules and the settings (11 tests) | Ready, do not edit |
| [tests/test_database.py](tests/test_database.py) | Acceptance tests for the migrations, the models and the data (11 tests) | Ready, do not edit |

## Tests

`pytest` runs all three test files, 36 tests in all. Until you fill in the TODOs, the tests fail: the routes, the rules and settings, and the database. Every test needs the migrated database, so until the migrations exist, every test reports an error at setup, not a failed assertion. One test passes from the start, once the database is in place: the default of 50 words, which the basics already set.
