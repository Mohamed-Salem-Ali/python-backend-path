# Study API

The first stage of an AI wrapper API, built in the FastAPI track. It stores summaries in a database and serves them over HTTP. The summary comes from a stand-in function for now. A real model call comes later, in the background.

The lessons are in [../10-basics/lesson.md](../10-basics/lesson.md) (routes), [../10-pydantic/lesson.md](../10-pydantic/lesson.md) (validation and settings), [../11-database/lesson.md](../11-database/lesson.md) (the database and migrations) and [../11-auth/lesson.md](../11-auth/lesson.md) (dependencies, passwords and tokens). This folder is the project you build while you work through them.

## Setup and run

From this folder:

```bash
pip install -r requirements.txt
```

Set the secret key first. The app signs its login tokens with it, and it refuses to start without one. Use a random string of at least 32 characters. In bash:

```bash
export STUDY_SECRET_KEY="replace-me-with-a-random-string-of-32-characters-or-more"
```

In PowerShell, use `$env:STUDY_SECRET_KEY = "..."` instead. Every command below reads the key, so set it in the same window.

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

Four settings come from the environment. `STUDY_SECRET_KEY` is required: it signs the login tokens, and it must be at least 32 characters. `STUDY_ACCESS_TOKEN_MINUTES` is how long a login token lasts, and it defaults to 30. `STUDY_MAX_WORDS` is the limit on a summary's words, and it defaults to 500. `STUDY_DATABASE_URL` is the database address, and it defaults to the SQLite file above.

## Layout

| Path | What it is | State |
|---|---|---|
| [app/main.py](app/main.py) | The app, the router includes, and the health route | TODO comments only (modules 10 and 11) |
| [app/routers/summaries.py](app/routers/summaries.py) | The summaries routes: create, list, fetch and delete | TODO comments only (module 10, then the database and the owner in module 11) |
| [app/routers/auth.py](app/routers/auth.py) | The register and login routes | TODO comments only (module 11, auth) |
| [app/routers/me.py](app/routers/me.py) | The signed-in user's routes: the user and their summaries | TODO comments only (module 11, auth) |
| [app/schemas.py](app/schemas.py) | The request and response models, and their validation rules | Basics ready; validation, row reading and the user shapes are TODO comments (Pydantic, database, auth) |
| [app/config.py](app/config.py) | Settings read from the environment: the database address, the secret key and the token lifetime | TODO comments only (Pydantic, database, auth) |
| [app/database.py](app/database.py) | The async engine, the session for each request, and the base class | TODO comments only (module 11) |
| [app/models.py](app/models.py) | The `Summary` and `User` tables | TODO comments only (module 11, the database and auth) |
| [app/security.py](app/security.py) | Password hashing, and creating and reading tokens | TODO comments only (module 11, auth) |
| [app/dependencies.py](app/dependencies.py) | The dependencies that read the signed-in user from a token | TODO comments only (module 11, auth) |
| [app/store.py](app/store.py) | The first in-memory storage. Delete it once no route uses it | Ready until module 11 replaces it |
| [app/summarizer.py](app/summarizer.py) | A stand-in for the AI call | Ready |
| [alembic.ini](alembic.ini), [migrations/env.py](migrations/env.py) | Alembic's settings and the migration environment | Ready |
| [migrations/versions/](migrations/versions/) | The migration files. You generate them (the database lesson, sections 4 and 5, then the auth lesson, section 4) | Empty until you generate them |
| [tests/conftest.py](tests/conftest.py) | Fixtures: a migrated test database, an empty table for each test, and a test client | Ready |
| [tests/test_basics.py](tests/test_basics.py) | Acceptance tests for the routes (14 tests) | Ready, do not edit |
| [tests/test_validation.py](tests/test_validation.py) | Acceptance tests for the rules and the settings (11 tests) | Ready, do not edit |
| [tests/test_database.py](tests/test_database.py) | Acceptance tests for the migrations, the models and the data (11 tests) | Ready, do not edit |
| [tests/test_auth.py](tests/test_auth.py) | Acceptance tests for the settings, passwords, tokens, protected routes and owners (22 tests) | Ready, do not edit |

## Tests

`pytest` runs all four test files, 58 tests in all. Until you fill in the TODOs, the tests fail: the routes, the rules and settings, the database, and the sign-in. Every test needs the migrated database, so until the migrations exist, every test reports an error at setup, not a failed assertion. Once the database is in place, one test passes from the start: the default of 50 words, which the basics already set. The auth tests also need the users migration (the auth lesson, section 4).
