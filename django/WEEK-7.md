# Week 7: Django REST Framework, middleware and signals

Goal by Saturday: expose Gameya as a REST API that anyone can read and only token holders can change, give every response a request id, and record payment and member changes in an audit log. Module 06 comes first: module 07's tests call the API root that module 06 adds.

Daily shape: **Learn 1–1.5 h → Build 1–1.5 h → Drill 20 min → Wrap-up 10 min** (see [the plan](../docs/12-week-plan.md)). On a short day (2 h), do Learn and Wrap-up only. The drills for this week are in [drills.md](../docs/drills.md#week-7).

Run the commands below from `django/gameya_site`.

| Day | Learn | Build / exercises | Drill |
|---|---|---|---|
| **1** | [06 DRF](06-drf/lesson.md) sections 1–4: serializers, viewsets, routers | Setup step: install DRF, add it to `requirements.txt` and `INSTALLED_APPS` (TODO 15), `migrate`, `SetupTests` passes. Then TODOs 16 and 17, the serializers | 1 easy problem |
| **2** | 06 sections 5–8: actions, authentication, permissions, pagination | TODO 18 (the permission class), TODO 19 (the page size), then TODOs 20 and 21, the viewsets | 1 easy problem |
| **3** | 06 sections 9–12: filtering, N+1 again, what token auth does not do | Only now TODO 22, the router and the token route; all 33 tests in `circles.tests.test_api` pass; get a token and call the API with `curl.exe` | 1 problem |
| **4** | [07 Middleware and signals](07-middleware-signals/lesson.md) sections 1–4: what middleware wraps, short-circuits, order | TODO 23 (`RequestIdMiddleware`), then TODO 27 (add it to `MIDDLEWARE`); `RequestIdMiddlewareTests` passes | 1 problem |
| **5** | 07 sections 5–10: signals, connecting receivers, when not to use a signal, testing both | TODO 26 (`AuditEntry` and its migration), TODO 24 (the receivers), TODO 25 (`ready()`); all 16 tests in `circles.tests.test_middleware_signals` pass | 1 problem |
| **6** | Review 06 and 07 | Check the request id with `curl.exe -i -H "X-Request-ID: my-test-1" http://127.0.0.1:8000/api/`; read one audit entry in the admin or the shell | 1 problem |
| **Review day** | Redo the weakest TODO from memory | Run the whole suite: `python manage.py test`; commit | Write 2–3 interview questions with your own answers, from [the question bank](../docs/interview-questions.md) |

Add the router (TODO 22) and the middleware setting (TODO 27) only after the classes they name exist. Both are read when the project loads, so a missing class breaks every test in every module, not just this one.

## Stretch goals
- Add a `ReviewSerializer` and `ReviewViewSet` for the lesson's book example, and check that a duplicate review returns 400 (module 06).
- Add a middleware that counts requests in a header, then explain why a global counter is wrong with several server processes (module 07).
- Write down which audit entries a bulk `QuerySet.delete()` produces, then check your answer in the shell.

## Daily wrap-up
```
Date:
Learned:
Confused by:
Tomorrow:
```

## Checkpoint (end of week)
Without notes you can:
- [ ] Say what a serializer does in each direction, and which fields you made read-only and why
- [ ] Explain what a viewset and a router generate, and add an extra endpoint with `@action`
- [ ] Tell 400, 401 and 403 apart, with one Gameya request for each
- [ ] Explain what token authentication protects, and what it leaves open
- [ ] Write a middleware class and say where in `MIDDLEWARE` it goes and why
- [ ] Explain why a signal receiver that is never imported does nothing
- [ ] Name one job a signal is good for and one it is not

## Notes for Week 8
Next week switches the test runner to pytest, measures and cuts the query count, and moves slow work into Celery. The API you built this week is one of the things the new tests check.
