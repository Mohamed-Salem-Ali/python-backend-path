# FastAPI (weeks 10–12)

In progress. You build an AI wrapper API (summaries, explanations, flashcards) with async SQLAlchemy 2.0, Alembic, Pydantic v2, JWT, background tasks, Docker and deployment. The first stage, the Study API, is in [study-api/](study-api/).

Start with the [syllabus](SYLLABUS.md). The week-by-week outline is in [the 12-week plan](../docs/12-week-plan.md).

## Weeks

| Week | Topics | Status | Needs first |
|---|---|---|---|
| 10 | Async Python, FastAPI basics, Pydantic v2 | In progress: [async Python](../python/12-concurrency-async/lesson.md) and [FastAPI basics](10-basics/lesson.md) are written. Pydantic is next | Python module 12 |
| 11 | Async SQLAlchemy and Alembic, dependency injection, JWT auth | Planned | Week 10 |
| 12 | Background work, async testing, Docker, deployment | Planned | Week 11 |

The syllabus lists nine topics across these three weeks. Lesson folders are created when each lesson is written.

## Files in this folder

| File | What it is |
|---|---|
| [SYLLABUS.md](SYLLABUS.md) | Core track, project, exit exam, advanced tier |
| [10-basics/](10-basics/) | Lesson: routing, parameters, response models and status codes |
| [study-api/](study-api/) | The project: the Study API, with its tests |
