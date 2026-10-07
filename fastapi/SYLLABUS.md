# FastAPI syllabus

Weeks 10–12 of the [12-week plan](../docs/12-week-plan.md). Prerequisites: the [Python exit exam](../python/SYLLABUS.md#exit-exam-i-know-python) (including async) and the DRF module from Django, for direct comparison.

**Level target:** design, test, containerize and deploy an async API, and explain when FastAPI is the better choice than Django.

**Project:** an AI wrapper API (summaries, explanations, flashcards) with users, saved results, rate limiting and background work.

## Core track

| Week | Module | You can… |
|---|---|---|
| 10 | Async Python | write and reason about `async`/`await`, the event loop, blocking vs non-blocking |
| 10 | FastAPI basics | routing, path/query/body parameters, response models, status codes |
| 10 | Pydantic v2 | validate input, define schemas, settings from environment variables |
| 11 | Database | async SQLAlchemy 2.0 sessions, models, relations, Alembic migrations |
| 11 | Dependency injection | build reusable dependencies (DB session, current user, rate limit) |
| 11 | Auth | password hashing, JWT access tokens, protected routes |
| 12 | Background work | `BackgroundTasks`, and when to reach for a real queue |
| 12 | Testing | async pytest, dependency overrides, a test database |
| 12 | Docker and deployment | Dockerfile, environment config, deploy to a real host |

## Exit exam: "I know FastAPI"
- [ ] Explain what happens when an async endpoint calls a blocking function, and how to fix it
- [ ] Build an endpoint with a request model, a response model and validation errors that read well
- [ ] Add an Alembic migration for a new column without breaking existing data
- [ ] Protect a route with JWT, and write tests for the allowed and denied cases using dependency overrides
- [ ] Stream or background a long-running AI call without blocking other requests
- [ ] Containerize the app and run it with environment-only configuration
- [ ] Write a one-page comparison with Django/DRF: where each is the better choice

## Advanced tier (after week 12)
- Production: Gunicorn with Uvicorn workers, timeouts, graceful shutdown, health checks
- Reliability: retries, idempotency keys, circuit breakers around third-party APIs
- Performance: connection pooling, caching with Redis, load testing, profiling
- Real time: WebSockets and server-sent events
- Observability: structured logging, tracing, metrics
- Architecture: layered design, repository pattern, background workers (Celery, ARQ)
