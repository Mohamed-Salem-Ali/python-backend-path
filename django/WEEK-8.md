# Week 8: Testing, performance and background tasks

Goal by Saturday: run the whole project under pytest with factories and fixtures, build the gameya summary with a fixed number of queries and cache it, and send the weekly unpaid-payments report from a Celery task.

Daily shape: **Learn 1–1.5 h → Build 1–1.5 h → Drill 20 min → Wrap-up 10 min** (see [the plan](../docs/12-week-plan.md)). On a short day (2 h), do Learn and Wrap-up only. The drills for this week are in [drills.md](../docs/drills.md#week-8).

Run the commands below from `django/gameya_site`. From this week on, `pytest` runs the tests; `python manage.py test` still works for the older ones.

| Day | Learn | Build / exercises | Drill |
|---|---|---|---|
| **1** | [08 Testing](08-testing/lesson.md) sections 1–5: two runners, `pytest.ini`, parametrize, fixtures, pytest-django's fixtures | `pip install -r requirements.txt`; TODO 28, `pytest.ini`; `pytest` now starts and runs the earlier modules' tests | 1 easy problem |
| **2** | 08 sections 6–12: factories, the test client, counting queries, settings for one test, coverage | TODO 29 (the factories), TODO 30 (the fixtures); all 26 tests in `circles/tests/test_pytest_suite.py` pass | 1 easy problem |
| **3** | [09 Caching and performance](09-caching-performance/lesson.md) sections 1–6: measure, N+1, `select_related`, `prefetch_related` | TODO 34 (`CACHES`), TODO 31 (`build_summary` with prefetching); count its queries in `manage.py shell` with one member, then two | 1 problem |
| **4** | 09 sections 7–10: the cache framework, invalidation, page caching | TODO 32 (`gameya_summary`), TODO 33 (`invalidate_summary` and its receivers); all 18 tests in `circles/tests/test_performance.py` pass | 1 problem |
| **5** | [10 Background tasks](10-background-tasks/lesson.md) sections 1–5: why work leaves the request, broker, worker and beat, writing and running a task | TODO 35 (`config/celery.py`), then TODO 36 (`config/__init__.py`), then TODO 37 (the settings and the beat schedule) | 1 problem |
| **6** | 10 sections 6–9: retries, beat, testing tasks, the project step | TODO 38a (`current_week`), 38b (`send_unpaid_report`), 38c (`queue_unpaid_reports`); all 16 tests in `circles/tests/test_tasks.py` pass | 1 problem |
| **Review day** | Break one thing on purpose: remove the prefetch, or change `Member.due()`. Read the failure, then undo it | Run `pytest` for the whole project; commit | Write 2–3 interview questions with your own answers, from [the question bank](../docs/interview-questions.md) |

Write TODO 36 only after TODO 35 works. `config/__init__.py` runs on every import of the project, so a broken Celery app there fails every test.

## Stretch goals
- Write one parametrized test for the audit log from week 7, with three cases built by your factories (module 08).
- Put `@cache_page(60)` on the gameya list view, prove a second request runs no queries, then explain the stale-data window and remove it (module 09).
- Start a real worker and beat locally with Redis and watch one scheduled report run (module 10).

## Daily wrap-up
```
Date:
Learned:
Confused by:
Tomorrow:
```

## Checkpoint (end of week)
Without notes you can:
- [ ] Say what `pytest.ini` must contain for pytest-django, and what breaks without it
- [ ] Write a fixture and a factory, and say when to use each
- [ ] Explain the N+1 problem and fix it with `select_related` or `prefetch_related`, choosing the right one
- [ ] Count a view's queries in a test, and say why the count matters more than the time
- [ ] Explain cache invalidation for the gameya summary: which changes clear it, and how
- [ ] Name the broker, the worker and beat, and say why a task takes an id, not a model object
- [ ] Explain how an eager-mode test can pass while production fails

## Notes for Week 9
Next week locks the project down (JWT, ownership, secure settings), deploys it, and turns it into a portfolio piece. Before you start, every test file from modules 02 to 10 should pass.
