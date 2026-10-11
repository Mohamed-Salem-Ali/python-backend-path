# Study API

The first stage of an AI wrapper API, built in the FastAPI track. It stores summaries in a database and serves them over HTTP. The summary comes from a stand-in function for now. A real model call comes later, in the background.

The lessons are in [../10-basics/lesson.md](../10-basics/lesson.md) (routes), [../10-pydantic/lesson.md](../10-pydantic/lesson.md) (validation and settings), [../11-database/lesson.md](../11-database/lesson.md) (the database and migrations) [../11-auth/lesson.md](../11-auth/lesson.md) (dependencies, passwords and tokens) and [../12-background/lesson.md](../12-background/lesson.md) (background work and async tests) and [../12-docker/lesson.md](../12-docker/lesson.md) (Docker and deployment). This folder is the project you build while you work through them.

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

## Run in a container

The `Dockerfile` in this folder runs the migrations, then starts the server. Build the image:

```bash
docker build -t study-api .
```

Create a volume for the database, then run the container with a secret key:

```bash
docker volume create study-data
```

```bash
docker run -d --name study-api -e STUDY_SECRET_KEY="replace-me-with-a-random-string-of-32-characters-or-more" -v study-data:/data -p 8000:8000 study-api
```

Section 7 of [the Docker lesson](../12-docker/lesson.md) lists the checks. The configuration comes from the environment, and the image holds no secret.

## Layout

| Path | What it is | State |
|---|---|---|
| [app/main.py](app/main.py) | The app, the router includes, and the health route | TODO comments only (modules 10 and 11) |
| [app/routers/summaries.py](app/routers/summaries.py) | The summaries routes: create, list, fetch and delete, and the flashcard routes | TODO comments only (module 10, then the database and the owner in module 11, the flashcard routes in module 12) |
| [app/routers/auth.py](app/routers/auth.py) | The register and login routes | TODO comments only (module 11, auth) |
| [app/routers/me.py](app/routers/me.py) | The signed-in user's routes: the user and their summaries | TODO comments only (module 11, auth) |
| [app/schemas.py](app/schemas.py) | The request and response models, and their validation rules | Basics ready; validation, row reading, the user shapes and the flashcard shapes are TODO comments (Pydantic, database, auth, background work) |
| [app/config.py](app/config.py) | Settings read from the environment: the database address, the secret key and the token lifetime | TODO comments only (Pydantic, database, auth) |
| [app/database.py](app/database.py) | The async engine, the session for each request, the base class, and the SQLite foreign-key setting | TODO comments only (module 11, and the foreign-key setting in module 12) |
| [app/models.py](app/models.py) | The `Summary`, `User` and `Flashcard` tables | TODO comments only (module 11, the database and auth; module 12 for flashcards) |
| [app/security.py](app/security.py) | Password hashing, and creating and reading tokens | TODO comments only (module 11, auth) |
| [app/dependencies.py](app/dependencies.py) | The dependencies that read the signed-in user from a token | TODO comments only (module 11, auth) |
| [app/services.py](app/services.py) | The flashcard job that runs in the background, and the dependency that supplies its maker | TODO comments only (module 12) |
| [app/flashcards.py](app/flashcards.py) | A stand-in for the flashcard maker: one card per sentence | Ready |
| [Dockerfile](Dockerfile) | The image: the Python version, the user, the port, the health check and the start command | TODO comments only (module 12, Docker) |
| [.dockerignore](.dockerignore) | The files the image build must not copy: secrets, local databases, virtual environments and tests | TODO comments only (module 12, Docker) |
| [app/store.py](app/store.py) | The first in-memory storage. Delete it once no route uses it | Ready until module 11 replaces it |
| [app/summarizer.py](app/summarizer.py) | A stand-in for the AI call | Ready |
| [alembic.ini](alembic.ini), [migrations/env.py](migrations/env.py) | Alembic's settings and the migration environment | Ready |
| [migrations/versions/](migrations/versions/) | The migration files. You generate them (the database lesson, sections 4 and 5, the auth lesson, section 4, and the background work lesson, section 4) | Empty until you generate them |
| [tests/conftest.py](tests/conftest.py) | Fixtures: a migrated test database, an empty table for each test, and a test client | Ready |
| [tests/test_basics.py](tests/test_basics.py) | Acceptance tests for the routes (14 tests) | Ready, do not edit |
| [tests/test_validation.py](tests/test_validation.py) | Acceptance tests for the rules and the settings (11 tests) | Ready, do not edit |
| [tests/test_database.py](tests/test_database.py) | Acceptance tests for the migrations, the models and the data (11 tests) | Ready, do not edit |
| [tests/test_auth.py](tests/test_auth.py) | Acceptance tests for the settings, passwords, tokens, protected routes and owners (22 tests) | Ready, do not edit |
| [tests/test_background.py](tests/test_background.py) | Acceptance tests for queueing, the background job, async tests and dependency overrides (18 tests) | Ready, do not edit |
| [tests/test_deployment.py](tests/test_deployment.py) | Acceptance tests for the image file and the ignore file, read as text (12 tests) | Ready, do not edit |

## Tests

`pytest` runs all six test files, 88 tests in all. Until you fill in the TODOs, the tests fail: the routes, the rules and settings, the database, the sign-in, the background work, and the image. Every test needs the migrated database, so until the migrations exist, every test reports an error at setup, not a failed assertion. Once the database is in place, three tests pass before you write the code: the default of 50 words, which the basics already set; the flashcard cascade check, once the flashcards migration exists; and the check that no secret is in the image, which holds until you add one. The auth tests need the users migration (the auth lesson, section 4). The background work tests need the flashcards migration (the background work lesson, section 4). The deployment tests read the Dockerfile as text, so they need no Docker.
