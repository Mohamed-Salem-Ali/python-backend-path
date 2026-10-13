# Week 10: Async Python, FastAPI basics and Pydantic

Goal by Saturday: reason about threads, processes and `async`/`await`, and build the first version of the Study API: four summary routes with request and response models, validation rules, and settings read from the environment.

Daily shape: **Learn 1–1.5 h → Build 1–1.5 h → Drill 20 min → Wrap-up 10 min** (see [the plan](../docs/12-week-plan.md)). On a short day (2 h), do Learn and Wrap-up only. The drills for this week are in [drills.md](../docs/drills.md#week-10).

## Setup (Day 3, 15 minutes)
The first two days use the Python track. From day 3, work in `fastapi/study-api` with its own virtual environment:

```bash
cd fastapi/study-api
python -m venv .venv
.venv\Scripts\Activate.ps1            # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pytest                                # every test errors at first: they are your to-do list
```

The tests need the database from week 11, so this week check your routes with `uvicorn app.main:app --reload` and the docs page at `http://127.0.0.1:8000/docs`. The [Study API README](study-api/README.md#tests) explains when each test file starts to pass.

| Day | Learn | Build / exercises | Drill |
|---|---|---|---|
| **1** | [Python 12 Concurrency and async](../python/12-concurrency-async/lesson.md) sections 1–4: waiting vs computing, the GIL, threads, processes | `python python/12-concurrency-async/exercises.py`, checks 1–4 | 1 easy problem |
| **2** | Python 12 sections 5–10: asyncio, `gather`, cancellation, queues, choosing | checks 5–10; the file prints `All checks passed` | 1 easy problem |
| **3** | [FastAPI basics](10-basics/lesson.md) sections 1–5: type hints, routing, path and query parameters, the body | Setup above; TODO 1 (create) and TODO 5 (include the router); try a POST from the docs page | 1 problem |
| **4** | Basics sections 6–10: response models, status codes, `def` or `async def`, the docs, testing a route | TODOs 2, 3 and 4 (list, fetch, delete), TODO 6 (`/health`); check each status code from the docs page | 1 problem |
| **5** | [Pydantic v2](10-pydantic/lesson.md) sections 1–5: checking data, coercion, constraints, validators, input vs output models | TODO 8, the rules on `SummaryIn`; send a blank text and an unknown field and read the 422 | 1 problem |
| **6** | Pydantic sections 6–8: settings from the environment, the docs, common mistakes | TODO 7, the `Settings` class; change `STUDY_MAX_WORDS` and watch the limit move | 1 problem |
| **Review day** | Redo the weakest async check from memory | Commit; write down which TODOs the tests will check once the database exists | Write 2–3 interview questions with your own answers, from [the question bank](../docs/interview-questions.md) |

## Stretch goals
- Time `exercises.py` check 1 with one thread and with ten, and explain the difference in one sentence (Python 12).
- Add a `GET /summaries/count` route, and decide where it must go in the file so `/{summary_id}` does not catch it (basics).
- Add a validator that refuses a text made only of digits, and show its message in the docs (Pydantic).

## Daily wrap-up
```
Date:
Learned:
Confused by:
Tomorrow:
```

## Checkpoint (end of week)
Without notes you can:
- [ ] Say when threads help, when processes help, and when neither does
- [ ] Explain what happens when an `async def` route calls a blocking function, and how to fix it
- [ ] Write a route with path, query and body parameters and a response model
- [ ] Pick the right status code for create, delete and not found, and raise it
- [ ] Explain lax coercion, and refuse fields a client should not send
- [ ] Read a setting from an environment variable with a prefix and a default

## Notes for Week 11
Next week replaces the in-memory store with a database and adds users. Once the first migration exists, the tests start to run, and this week's routes are checked for real.
