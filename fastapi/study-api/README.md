# Study API

The first stage of an AI wrapper API, built in the FastAPI track. It stores summaries in a database and serves them over HTTP. By default the summaries and flashcards come from small stand-in functions, so the project runs with no API key and no cost. The bonus module adds a real Gemini call behind the same dependencies, chosen by a setting, and rate limits on login and on creating summaries.

The lessons are in [../10-basics/lesson.md](../10-basics/lesson.md) (routes), [../10-pydantic/lesson.md](../10-pydantic/lesson.md) (validation and settings), [../11-database/lesson.md](../11-database/lesson.md) (the database and migrations), [../11-auth/lesson.md](../11-auth/lesson.md) (dependencies, passwords and tokens), [../12-background/lesson.md](../12-background/lesson.md) (background work and async tests), [../12-docker/lesson.md](../12-docker/lesson.md) (Docker and deployment) and, as a bonus, [../13-ai-and-limits/lesson.md](../13-ai-and-limits/lesson.md) (a real model and rate limits). This folder is the project you build while you work through them.

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

Four settings come from the environment, and the bonus module adds five more. `STUDY_SECRET_KEY` is required: it signs the login tokens, and it must be at least 32 characters. `STUDY_ACCESS_TOKEN_MINUTES` is how long a login token lasts, and it defaults to 30. `STUDY_MAX_WORDS` is the limit on a summary's words, and it defaults to 500. `STUDY_DATABASE_URL` is the database address, and it defaults to the SQLite file above. From the bonus module: `STUDY_AI_PROVIDER` is `stub` (the default) or `gemini`; `STUDY_AI_API_KEY` is required with `gemini`, and is never written to a file; `STUDY_AI_MODEL` defaults to `gemini-3.5-flash-lite`; `STUDY_AI_TIMEOUT_SECONDS` defaults to 20; and `STUDY_RATE_LIMIT_PER_MINUTE` defaults to 10, where 0 turns the limit off.

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
| [app/routers/summaries.py](app/routers/summaries.py) | The summaries routes: create, list, fetch and delete, and the flashcard routes | TODO comments only (module 10, then the database and the owner in module 11, the flashcard routes in module 12, the summarizer dependency and the rate limit in bonus module 13) |
| [app/routers/auth.py](app/routers/auth.py) | The register and login routes | TODO comments only (module 11, auth; the login rate limit in bonus module 13) |
| [app/routers/me.py](app/routers/me.py) | The signed-in user's routes: the user and their summaries | TODO comments only (module 11, auth) |
| [app/schemas.py](app/schemas.py) | The request and response models, and their validation rules | Basics ready; validation, row reading, the user shapes and the flashcard shapes are TODO comments (Pydantic, database, auth, background work) |
| [app/config.py](app/config.py) | Settings read from the environment: the database address, the secret key, the token lifetime, and the model and rate-limit settings | TODO comments only (Pydantic, database, auth, bonus module 13) |
| [app/database.py](app/database.py) | The async engine, the session for each request, the base class, and the SQLite foreign-key setting | TODO comments only (module 11, and the foreign-key setting in module 12) |
| [app/models.py](app/models.py) | The `Summary`, `User` and `Flashcard` tables | TODO comments only (module 11, the database and auth; module 12 for flashcards) |
| [app/security.py](app/security.py) | Password hashing, and creating and reading tokens | TODO comments only (module 11, auth) |
| [app/dependencies.py](app/dependencies.py) | The dependencies that read the signed-in user from a token | TODO comments only (module 11, auth) |
| [app/services.py](app/services.py) | The flashcard job that runs in the background, and the dependency that supplies its maker | TODO comments only (module 12; choosing the maker by setting in bonus module 13) |
| [app/flashcards.py](app/flashcards.py) | A stand-in for the flashcard maker: one card per sentence | Ready |
| [app/ai.py](app/ai.py) | The Gemini client, the summarizer and flashcard maker built on it, and the dependency that chooses the summarizer | TODO comments only (bonus module 13) |
| [app/ratelimit.py](app/ratelimit.py) | The sliding-window limiter and the dependency that answers 429 | TODO comments only (bonus module 13) |
| [Dockerfile](Dockerfile) | The image: the Python version, the user, the port, the health check and the start command | TODO comments only (module 12, Docker) |
| [.dockerignore](.dockerignore) | The files the image build must not copy: secrets, local databases, virtual environments and tests | TODO comments only (module 12, Docker) |
| [app/store.py](app/store.py) | The first in-memory storage. Delete it once no route uses it | Ready until module 11 replaces it |
| [app/summarizer.py](app/summarizer.py) | A stand-in for the AI call, and the default | Ready |
| [alembic.ini](alembic.ini), [migrations/env.py](migrations/env.py) | Alembic's settings and the migration environment | Ready |
| [migrations/versions/](migrations/versions/) | The migration files. You generate them (the database lesson, sections 4 and 5, the auth lesson, section 4, and the background work lesson, section 4) | Empty until you generate them |
| [tests/conftest.py](tests/conftest.py) | Fixtures: a migrated test database, an empty table for each test, and a test client | Ready |
| [tests/test_basics.py](tests/test_basics.py) | Acceptance tests for the routes (14 tests) | Ready, do not edit |
| [tests/test_validation.py](tests/test_validation.py) | Acceptance tests for the rules and the settings (11 tests) | Ready, do not edit |
| [tests/test_database.py](tests/test_database.py) | Acceptance tests for the migrations, the models and the data (11 tests) | Ready, do not edit |
| [tests/test_auth.py](tests/test_auth.py) | Acceptance tests for the settings, passwords, tokens, protected routes and owners (22 tests) | Ready, do not edit |
| [tests/test_background.py](tests/test_background.py) | Acceptance tests for queueing, the background job, async tests and dependency overrides (18 tests) | Ready, do not edit |
| [tests/test_deployment.py](tests/test_deployment.py) | Acceptance tests for the image file and the ignore file, read as text (12 tests) | Ready, do not edit |
| [tests/test_ai.py](tests/test_ai.py) | Acceptance tests for the model settings, the client, the choice of maker, the 502, and the rate limits (29 tests, bonus module) | Ready, do not edit |

## Tests

`pytest` runs all seven test files, 117 tests in all: 88 for weeks 10 to 12, and 29 for the bonus module. Until you fill in the TODOs, the tests fail: the routes, the rules and settings, the database, the sign-in, the background work, and the image. Every test needs the migrated database, so until the migrations exist, every test reports an error at setup, not a failed assertion. Once the database is in place, three tests pass before you write the code: the default of 50 words, which the basics already set; the flashcard cascade check, once the flashcards migration exists; and the check that no secret is in the image, which holds until you add one. The auth tests need the users migration (the auth lesson, section 4). The background work tests need the flashcards migration (the background work lesson, section 4). The deployment tests read the Dockerfile as text, so they need no Docker. The bonus module's tests never call a real model, so they need no key; the suite turns the rate limit off in `tests/conftest.py`, and the rate-limit tests switch on a limiter of their own.

## What I learned

The project uses the ideas below, and each one is taught in a lesson in this course. When you finish, rewrite this list in your own words: what surprised you, and what you would change.

- Routes, path and query parameters, response models and status codes: [basics](../10-basics/lesson.md)
- Validation with Pydantic, and settings read from the environment: [Pydantic](../10-pydantic/lesson.md)
- Async SQLAlchemy and Alembic migrations: [database](../11-database/lesson.md)
- Dependencies, password hashing, signed tokens and protected routes: [auth](../11-auth/lesson.md)
- Background work, cascading deletes in SQLite, async tests and dependency overrides: [background work](../12-background/lesson.md)
- A Dockerfile, a non-root user, health checks and volumes: [Docker](../12-docker/lesson.md)
- Where Django and FastAPI differ for an app like this one: [comparison](../12-comparison/comparison.md)
- Calling a model's API safely, testing it without the network, and rate limits: [a real model and rate limits](../13-ai-and-limits/lesson.md)
