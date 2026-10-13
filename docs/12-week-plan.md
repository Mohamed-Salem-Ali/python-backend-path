# 12-Week Plan: Python → Django → FastAPI

Started: 2026-10-07 (week 1). The module list is in the [README](../README.md); this file says **when**.

**Goals (all four):** truly master it, be interview-ready, be freelance-ready, ship portfolio projects.
**Rhythm:** 6 days/week, 2–5 h/day (about 3 h average). One day off. Starting level: beginner/rusty, so Python is taught from fundamentals.

## Daily shape (about 3 h)

| Block | Time | What |
|---|---|---|
| Learn | 1–1.5 h | One concept from the module: read, then type every example yourself (no copy-paste) |
| Build | 1–1.5 h | Apply it in the week's project; commit small |
| Drill | 20 min | One coding challenge from [drills.md](drills.md) (HackerRank, easy ones) |
| Wrap-up | 10 min | Write 3 lines: what I learned, what confused me, tomorrow's step |

On a 2 h day: do Learn + Wrap-up. On a 5 h day: add a second Build block, never skip the wrap-up.
**Day 6 of each week = review + ship:** redo the weakest exercise from memory, write 2–3 interview questions with your own answers, and tick the week's checkpoint.

## Phase 0: Python fundamentals (weeks 1–4)

| Week | Modules | Build (mini project) |
|---|---|---|
| 1 | 01 Environment, 02 Syntax and types, 03 Collections, 04 Control flow | Number and text utilities: a word counter, a contacts dictionary |
| 2 | 05 Functions, 06 Modules and stdlib, 08 Error handling | Gameya calculator CLI: payout, due amount and the Sunday-to-Thursday pay window as pure functions |
| 3 | 07 OOP, 09 Iterators and generators, 10 Decorators | Model Gameya as classes (`Gameya`, `Member`, `Payment`) with properties and `__str__` |
| 4 | 11 Typing, 13 Testing (pytest), 14 Packaging, 15 Capstone | **Task Tracker CLI**: files, errors, tests, `pyproject.toml`, type hints |

(12 Concurrency and async moves to week 10, right before FastAPI, where it is needed.)
**Checkpoint end of week 4:** the CLI has tests that pass, and you can explain closures, generators, decorators and the MRO without notes.

## Phase 1: Django (weeks 5–9)

| Week | Modules | Build |
|---|---|---|
| 5 | 01 Architecture (MTV, project vs app), 02 Models and ORM | Start **Gameya in Django**: models, migrations, relations, QuerySets, a `status` method per cell |
| 6 | 03 Admin and forms, 04 Views, 05 Templates | Admin for members and payments, the public gameya page, forms with validation |
| 7 | 06 DRF: serializers, viewsets, permissions, pagination; 07 Middleware and signals | Expose Gameya as a REST API with token auth, then a request id on every response and an audit log via signals |
| 8 | 08 Testing in Django, 09 Caching and performance, 10 Background tasks (Celery eager) | Tests with pytest-django and factories, kill the N+1 queries with `select_related` and `prefetch_related`, the weekly unpaid-payments report |
| 9 | 11 Auth and security, 12 Deployment, 13 Capstone | JWT and ownership permissions, security review, deploy to Render. **Portfolio project 1** |

The modules run in number order. Each one builds on the code of the one before: module 07's tests, for example, call the API root that module 06 adds.

**Checkpoint end of week 9:** Gameya runs in production on Django. You can explain why `select_related` fixes N+1 and how a migration works.

## Phase 2: FastAPI (weeks 10–12)

| Week | Focus | Build |
|---|---|---|
| 10 | Python async (module 12), FastAPI basics, Pydantic v2 | Scaffold the API, first endpoints, request and response models |
| 11 | Async SQLAlchemy 2.0, Alembic, JWT auth, dependency injection | **Study API**, the AI wrapper project: saved summaries in a database, users, login and protected routes |
| 12 | Background tasks, pytest for async, Docker, deployment | Flashcards made in the background, async tests, Dockerfile, deploy. **Portfolio project 2**. Compare it with the Django version in a short write-up |

The Study API's summaries and flashcards come from small stand-in functions through week 12, so the course runs with no API key and no cost. A bonus module after week 12, [a real model and rate limits](../fastapi/13-ai-and-limits/lesson.md), puts a Gemini call behind the same dependencies and limits logins and model calls per caller. Its tests fake the model, so it still needs no key.

**Checkpoint end of week 12:** two deployed projects, a README for each, and a blog-style "Django vs FastAPI, what I learned" note for your portfolio.

## Running through all weeks
- 1 coding challenge a day (Drill block), from [drills.md](drills.md) (easy ones first).
- 2–3 interview questions each Day 6, with answers in your own words.
- A 5-minute weekly reflection, from [weekly-reflection.md](weekly-reflection.md).
- Test first, then build: from week 4 on, every project gets tests as you go.

## Freelance and portfolio tie-in
- Week 9: add Gameya (Django) to the portfolio next to the Next.js version. The settings, decisions and known gaps are in [gameya-deployment-notes.md](gameya-deployment-notes.md).
- Week 12: add the FastAPI project and the comparison note.
- After week 12 (optional): a small client-style project, such as a booking system or an invoice tracker.

## If you fall behind
Don't cram. Drop the extra Build time, never the Learn block or the wrap-up, and let a phase slip by up to one week. The checkpoints matter more than the dates.
