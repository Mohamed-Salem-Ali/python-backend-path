# Week 9: Auth and security, deployment, and the capstone

Goal by Saturday: Gameya runs on a real host with JWT login, ownership rules and production settings, and you have a README, a security review and a case study you can show. This is **portfolio project 1** and the last week of the Django phase.

Daily shape: **Learn 1–1.5 h → Build 1–1.5 h → Drill 20 min → Wrap-up 10 min** (see [the plan](../docs/12-week-plan.md)). On a short day (2 h), do Learn and Wrap-up only. The drills for this week are in [drills.md](../docs/drills.md#week-9). Keep [the deployment notes](../docs/gameya-deployment-notes.md) open on days 3 and 4.

Run the commands below from `django/gameya_site`.

| Day | Learn | Build / exercises | Drill |
|---|---|---|---|
| **1** | [11 Auth and security](11-auth-security/lesson.md) sections 1–4: the threats, authentication, JWT with simplejwt, authorization | `pip install -r requirements.txt`; TODO 39 (`Gameya.organiser` and its migration), TODO 40 (`IsStaffOrOrganiser`), TODO 41 (`perform_update`), TODO 42 (the JWT routes and `SIMPLE_JWT`) | 1 easy problem |
| **2** | 11 sections 5–8: CSRF, XSS, secure settings, the security review | TODO 43 (production settings); all 19 tests in `circles/tests/test_security.py` pass; `check --deploy` with the production variables; fill in [security-review.md](11-auth-security/security-review.md) | 1 easy problem |
| **3** | [12 Deployment](12-deployment/lesson.md) sections 1–5: the parts of a deployed app, static files, the database URL, the app server | TODOs 44 and 45 (settings), TODO 46 (`render.yaml`), TODO 47 (`requirements.txt`); all 9 tests in `circles/tests/test_deployment.py` pass | 1 problem |
| **4** | 12 sections 6–8: Render, checking a deploy, after the deploy | Deploy on Render from the dashboard; run the smoke tests; fill in [deploy-checklist.md](12-deployment/deploy-checklist.md) with the live URL and the two log lines | Repeat a weak problem |
| **5** | [13 Capstone](13-capstone/lesson.md) sections 1–3: freeze, measure, explain | Run every test file and record the results; write down the query counts and the open security rows | Repeat a weak problem |
| **6** | 13 sections 4–7: the case study, the README, the portfolio entry, the three-minute talk | Fill in the [case study template](13-capstone/case-study-template.md); finish the [project README](gameya_site/README.md) with the live URL; say the talk out loud once | Repeat a weak problem |
| **Review day** | Go through the [Django exit exam](SYLLABUS.md#exit-exam-i-know-django) and the week 9 checkpoint in the [weekly reflection](../docs/weekly-reflection.md) | Commit; add the project to your portfolio | Write 2–3 interview questions with your own answers, from [the question bank](../docs/interview-questions.md) |

The deploy on day 4 is the step most likely to take longer than planned. If it does, let the capstone slide into the first days of week 10. A deployed project with a short write-up is worth more than a long write-up of a project that does not run.

## Stretch goals
- Close the open security row for the payment form: require a login, and update the module 04 tests that post anonymously (module 11).
- Add rate limiting to the JWT login and record it in `security-review.md`.
- Add a Celery worker to the Render plan, and note the cost of running it (module 10 and 12).

## Daily wrap-up
```
Date:
Learned:
Confused by:
Tomorrow:
```

## Checkpoint (end of week)
Without notes you can:
- [ ] Say how a session, a token and a JWT differ, and which one a browser form uses
- [ ] Name DRF's two permission checks, and say which one sees the object
- [ ] Explain why a token API needs no CSRF token, and a form does
- [ ] List the parts of a deployed Django app, and say which setting controls each
- [ ] Explain why the bind address is `0.0.0.0:$PORT` and why WhiteNoise is needed
- [ ] Open a missing page on the live site and say which setting keeps the traceback hidden
- [ ] Explain why `select_related` fixes N+1 and how a migration works (the plan's week 9 checkpoint)
- [ ] Give the three-minute talk about Gameya without notes

## Notes for Week 10
The FastAPI phase starts with Python module 12, concurrency and async, then rebuilds a small API in FastAPI. Keep Gameya deployed: the week 12 comparison note refers back to it.
