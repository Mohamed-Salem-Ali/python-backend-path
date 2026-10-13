# Week 11: The database, dependencies and auth

Goal by Saturday: the Study API keeps its summaries in a database through async SQLAlchemy, changes its schema only through Alembic migrations, and lets users register, log in with a JWT, and see their own summaries.

Daily shape: **Learn 1–1.5 h → Build 1–1.5 h → Drill 20 min → Wrap-up 10 min** (see [the plan](../docs/12-week-plan.md)). On a short day (2 h), do Learn and Wrap-up only. The drills for this week are in [drills.md](../docs/drills.md#week-11).

Work in `fastapi/study-api`. Run `pip install -r requirements.txt` on day 1, and again on day 4.

| Day | Learn | Build / exercises | Drill |
|---|---|---|---|
| **1** | [The database](11-database/lesson.md) sections 1–3: why a database, the engine and a session per request, models | TODO 12 (`database_url`), TODO 9 (`Base`, the engine, `get_session`), TODO 10 (the `Summary` model) | 1 easy problem |
| **2** | Database sections 4–5: migrations, adding a column that old rows need | Generate the first migration and the "add language" one, read both, run `alembic upgrade head`; the tests now start instead of erroring | 1 easy problem |
| **3** | Database sections 6–8: queries in async routes, testing against a database, common mistakes | TODO 11 (the routes use the database), TODO 13 (`from_attributes`); all 11 tests in `tests/test_database.py` pass, and so do the basics and validation tests | 1 problem |
| **4** | [Auth](11-auth/lesson.md) sections 1–3: dependencies, hashing passwords, signed tokens | Set `STUDY_SECRET_KEY`; TODO 14 (the auth settings), TODO 16 (`app/security.py`) | 1 problem |
| **5** | Auth sections 4–5: the users table, register and login, `get_current_user` | TODO 15 (`User`) and the users migration, TODO 17 (the user shapes), TODO 18 (the dependencies), TODO 19 (register and login) | 1 problem |
| **6** | Auth sections 6–10: dependencies of dependencies, optional users, overrides in tests, what is not covered | TODO 20 (`/me` routes), TODO 21 (the owner on create), TODO 22 (include the routers); all 22 tests in `tests/test_auth.py` pass, 58 in all | 1 problem |
| **Review day** | Redo the weakest TODO from memory | Register, log in and call `/me` from the docs page with the Authorize button; commit | Write 2–3 interview questions with your own answers, from [the question bank](../docs/interview-questions.md) |

Generate each migration only after its model is written, then read the file before you apply it. A migration that does not match the models fails a guard test, and that failure is the hint to read it again.

## Stretch goals
- Add a `title` column with a migration that fills a value for the old rows, then step back with `alembic downgrade -1` and forward again (database).
- Make the list route return the total count in a response header, using one extra query (database).
- Add a `DELETE /me` route that removes the user and their summaries, with a test for each case (auth).

## Daily wrap-up
```
Date:
Learned:
Confused by:
Tomorrow:
```

## Checkpoint (end of week)
Without notes you can:
- [ ] Explain why each request gets its own session, and how the dependency closes it
- [ ] Write a model with `Mapped` types, and say what `expire_on_commit=False` changes
- [ ] Add a column with a migration that keeps the existing rows, and roll it back
- [ ] Explain why passwords are hashed and not encrypted, and why hashing runs in a thread pool
- [ ] Say what is inside a JWT, what the signature proves, and what it does not hide
- [ ] Protect a route with a dependency, and test the allowed and denied cases with an override

## Notes for Week 12
Next week makes flashcards in the background, tests async code, and ships the API in a container. It is portfolio project 2, so keep the commits small and the README current.
