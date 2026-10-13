# FastAPI (weeks 10–12)

All three weeks are written. You build the Study API, an AI wrapper API (saved summaries, users, flashcards made in the background) with async SQLAlchemy 2.0, Alembic, Pydantic v2, JWT, background tasks, Docker and deployment. The project is in [study-api/](study-api/). The AI part is a stand-in function, so it runs with no API key; a real model call is in the syllabus's advanced tier.

Start with [WEEK-10.md](WEEK-10.md), and read the [syllabus](SYLLABUS.md) for what the track covers. The overview of all twelve weeks is in [the 12-week plan](../docs/12-week-plan.md).

## Weeks

| Week | Topics | Status | Needs first |
|---|---|---|---|
| 10 | Async Python, FastAPI basics, Pydantic v2 | Written: [async Python](../python/12-concurrency-async/lesson.md), then [FastAPI basics](10-basics/lesson.md) and [Pydantic](10-pydantic/lesson.md) | Python module 12 |
| 11 | Async SQLAlchemy and Alembic, dependency injection, JWT auth | Written: [the database](11-database/lesson.md), then [dependencies and auth](11-auth/lesson.md) | Week 10 |
| 12 | Background work, async testing, Docker, deployment | Written: [background work and testing](12-background/lesson.md), then [Docker and deployment](12-docker/lesson.md), and the [Django vs FastAPI comparison](12-comparison/comparison.md) | Week 11 |

The syllabus lists nine topics across these three weeks. The folder names start with the week number, so `11-database` and `11-auth` are both week 11. Do the database before auth, and background work before Docker.

## Files in this folder

| File | What it is |
|---|---|
| [SYLLABUS.md](SYLLABUS.md) | Core track, project, exit exam, advanced tier |
| [WEEK-10.md](WEEK-10.md) to [WEEK-12.md](WEEK-12.md) | Weekly goals and daily plan, one file per week |
| [10-basics/](10-basics/) | Lesson: routing, parameters, response models and status codes |
| [10-pydantic/](10-pydantic/) | Lesson: validation rules, input and output schemas, and settings from the environment |
| [11-database/](11-database/) | Lesson: the async engine and sessions, models, Alembic migrations, and testing against a database |
| [11-auth/](11-auth/) | Lesson: dependencies, password hashing, JWT tokens, protected routes, and routes that take an optional user |
| [12-background/](12-background/) | Lesson: `BackgroundTasks`, a job with its own session, foreign-key cascades, dependency overrides, and async tests |
| [12-docker/](12-docker/) | Lesson, deploy checklist and case-study template: the image, configuration from the environment, volumes, health checks, and deploying |
| [12-comparison/](12-comparison/) | The comparison of Django and FastAPI, where each is the better choice, and a template for your own blog note |
| [study-api/](study-api/) | The project: the Study API, with its tests |
