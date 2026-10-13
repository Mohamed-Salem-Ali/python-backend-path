# Week 12: Background work, async tests, Docker and the comparison

Goal by Saturday: the Study API makes flashcards after the response is sent, its tests cover that work and swap dependencies, it runs in a container with its settings from outside, and you have a short note comparing it with the Django project. This is **portfolio project 2** and the last week of the course.

Daily shape: **Learn 1–1.5 h → Build 1–1.5 h → Drill 20 min → Wrap-up 10 min** (see [the plan](../docs/12-week-plan.md)). On a short day (2 h), do Learn and Wrap-up only. The drills for this week are in [drills.md](../docs/drills.md#week-12).

Work in `fastapi/study-api`. Run `pip install -r requirements.txt` on day 1. Days 3 and 4 need Docker.

| Day | Learn | Build / exercises | Drill |
|---|---|---|---|
| **1** | [Background work and testing](12-background/lesson.md) sections 1–4: after the response, queueing, a session for the job, foreign keys and cascades | TODO 23 (SQLite foreign keys), TODO 24 (`Flashcard`) and the flashcards migration, TODO 25 (the two shapes) | 1 easy problem |
| **2** | Background sections 5–9: the maker as a dependency, failures and retries, testing background work, real queues | TODO 26 (`app/services.py`), TODO 27 (the flashcard routes); all 18 tests in `tests/test_background.py` pass, 76 in all | 1 easy problem |
| **3** | [Docker and deployment](12-docker/lesson.md) sections 1–6: images and containers, the Dockerfile, a non-root user, configuration, volumes, health checks | TODO 28 (`Dockerfile`), TODO 29 (`.dockerignore`); all 12 tests in `tests/test_deployment.py` pass, 88 in all (the 29 in `tests/test_ai.py` belong to the bonus module) | 1 problem |
| **4** | Docker sections 7–10: build, run and check, deploying, what is not covered | Build and run the image, check `/health`, the user and the volume; deploy to a host and fill in the [deploy checklist](12-docker/deploy-checklist.md) | 1 problem |
| **5** | [Django vs FastAPI](12-comparison/comparison.md): read it and run its checks | Write your own note from the [blog note template](12-comparison/portfolio-note-template.md), using your numbers, not the course's | Repeat a weak problem |
| **6** | Review the week | Fill in the [case study template](12-docker/case-study-template.md); rewrite the "What I learned" list in the [Study API README](study-api/README.md#what-i-learned) in your own words | Repeat a weak problem |
| **Review day** | Go through the [FastAPI exit exam](SYLLABUS.md#exit-exam-i-know-fastapi) and the week 12 checkpoint in the [weekly reflection](../docs/weekly-reflection.md) | Commit; add the project and the note to your portfolio | Write 2–3 interview questions with your own answers, from [the question bank](../docs/interview-questions.md) |

As in week 9, the deploy on day 4 can run long. Let the note and the case study slip a day or two rather than skip the deploy.

## Stretch goals
- Make the flashcard job safe to run twice for the same summary, and add a test that runs it twice (background work).
- Run the container with a read-only file system except for `/data`, and note what had to change (Docker).
- Start the bonus module, [a real model and rate limits](13-ai-and-limits/lesson.md): a Gemini call behind the maker dependency, and rate limits on login and on model calls.

## Daily wrap-up
```
Date:
Learned:
Confused by:
Tomorrow:
```

## Checkpoint (end of week)
Without notes you can:
- [ ] Say what `BackgroundTasks` guarantees and what it loses on a restart, and when to move to a real queue
- [ ] Explain why the background job opens its own session instead of using the request's
- [ ] Swap a dependency in a test, and write an async test with anyio
- [ ] Explain the order of the Dockerfile instructions in terms of layer caching
- [ ] Say why the container runs as a non-root user, and where its data lives
- [ ] Name two things Django gives you that FastAPI does not, and two the other way round
- [ ] Two deployed projects, a README for each, and a published comparison note (the plan's week 12 checkpoint)

## After week 12
The [12-week plan](../docs/12-week-plan.md#freelance-and-portfolio-tie-in) suggests a small client-style project next. Before that, the bonus module [a real model and rate limits](13-ai-and-limits/lesson.md) finishes the Study API as a real AI wrapper. Each track's syllabus also has an advanced tier for going deeper.
