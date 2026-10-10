# Module 11 (FastAPI): The database

By the end you can keep data in a database with async SQLAlchemy 2.0, write a model, change the schema with an Alembic migration that keeps existing rows, and test the routes against a real database. The project is `fastapi/study-api`.

**Before you start:** finish the FastAPI basics and Pydantic lessons (`../10-basics/lesson.md`, `../10-pydantic/lesson.md`), and the async lesson of the Python track (`../../python/12-concurrency-async/lesson.md`). Every database call in this module is `await`ed.

**Setup:** from `fastapi/study-api`, install the requirements again. This module adds SQLAlchemy's asyncio extra (which needs `greenlet`), `aiosqlite` for SQLite, and Alembic:

```bash
pip install -r requirements.txt
```

Run this module's tests with `pytest tests/test_database.py`. All 11 should pass when you finish. A bare `pytest` also runs the auth tests from the next module, which fail until you finish that module.

**How to read the examples:** the examples use a made-up `notes` app. It is not part of the Study API.

## 1. Why a database
The summaries so far live in a Python dict. A restart loses them, and two server processes would each have their own copy. A database keeps the rows outside the process, and the app asks it for what it needs. SQLAlchemy is the Python library that writes the SQL for you. Its 2.0 style uses type hints on the models and `select(...)` for queries, and the async version lets a route wait for the database without blocking other requests.

## 2. The engine and a session per request
The engine knows the database address and keeps a pool of connections. A session is one unit of work: it tracks the objects you add or change, and it sends them in one transaction when you commit.

```python
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

engine = create_async_engine("sqlite+aiosqlite:///./notes.db")
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    async with SessionLocal() as session:
        yield session
```

Routes get a session with `Depends(get_session)`. FastAPI runs `get_session` for each request and closes the session when the request ends. Module 11's dependencies are covered in depth in the next module; for now, read it as "give me a session".

`expire_on_commit=False` matters in async code. By default, a commit marks every loaded object as expired, and reading an expired attribute loads it from the database. In async code that load cannot happen implicitly, and it fails with a `MissingGreenlet` error. Keep the default off, and call `await session.refresh(obj)` when you need a value the database set.

**Try it:** in the Study API, remove the `expire_on_commit=False` argument from `app/database.py`, and remove the `session.refresh` line from the create route. Run `pytest tests/test_basics.py -k 201`. The response fails with `MissingGreenlet`. Put both lines back, and the test passes again.

## 3. A model is a class that describes a table
```python
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Note(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    priority: Mapped[int] = mapped_column(default=1, server_default="1")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
```

A `Mapped[...]` type hint sets the column's type and whether it can be empty. `default=` is a value the Python code sets when it creates the object. `server_default=` is a value the database sets when it inserts the row. The two differ: a row written by another program, or a row from before a column existed, gets only the server default. That difference is why the `created_at` column above uses a server default, and why section 5 depends on one.

## 4. Migrations: the database changes with the code
A migration is a file that changes the schema from one version to the next. Alembic keeps a list of them, and records which one the database has reached. Two rules keep this safe: never edit a migration that has run, and write a new one for each change.

`alembic.ini` points at the `migrations/` folder. `migrations/env.py` reads the database address from the settings, so the app and Alembic use one address. Autogenerate compares the models with the database and writes the difference:

```bash
alembic revision --autogenerate -m "create summaries"
alembic upgrade head
```

The first command writes a file into `migrations/versions/`. Read it before you run the second. The second applies every migration that the database has not run yet. `alembic downgrade -1` undoes the last one.

**Try it:** write the `Summary` model without the `language` column (the lesson's Study API stub has the fields), run the first command, and open the new file. Find the line that creates the table. Then run `alembic upgrade head`, and check the table with `sqlite3 study.db ".schema summaries"` if you have `sqlite3`, or with `pytest tests/test_database.py::test_upgrade_creates_the_summaries_table`.

## 5. Adding a column that old rows need
Now add `language` to the model, with a default in Python and in the database:

```python
language: Mapped[str] = mapped_column(String(8), default="en", server_default="en")
```

Run `alembic revision --autogenerate -m "add language"`. The generated file uses `batch_alter_table`. Batch mode lets Alembic make changes that SQLite cannot make in place, by copying the table when it has to. Adding a column with a default is a plain `ALTER TABLE`. The `server_default="en"` in the migration is what fills the column for the rows that already exist. Without it, the new column is `NOT NULL` with no default, and SQLite refuses the change: `Cannot add a NOT NULL column with default value NULL`.

Autogenerate writes what the model says. If the model lacks the server default, the migration lacks it too. The test `test_the_language_default_reaches_rows_written_before_the_column` checks this: it downgrades, writes a row the old way, upgrades again, and reads `en` back. The test `test_the_migrations_match_the_models` also compares the server defaults, so a model and a migration cannot quietly drift apart.

**Try it:** delete the `server_default="en"` from the model, generate a revision, and read it. Then run `pytest tests/test_database.py` and find which test fails, and why.

## 6. Queries in async routes
Each database call is awaited:

```python
session.add(summary)  # no await: it only records the change
await session.commit()  # writes the transaction
await session.refresh(summary)  # reloads values the database set, such as created_at

result = await session.scalars(select(Summary).order_by(Summary.id).offset(offset).limit(limit))
rows = result.all()

row = await session.get(Summary, summary_id)  # by primary key; None when missing
await session.delete(row)
await session.commit()
```

A query that is never committed is never saved: the session closes and the changes are discarded. A call you forgot to `await` does nothing, and Python warns about it. Both mistakes are in the tests: the create and delete tests fail if the commit is missing.

**Try it:** remove the `await session.commit()` from the create route, and run `pytest tests/test_database.py`. Count the failures, and explain why the list test still passes on its own.

## 7. Testing against a database
The test suite needs a real database, not a fake, because a fake would not check the SQL or the migrations. The study project does three things:

- The conftest sets `STUDY_DATABASE_URL` to a file in a temporary folder, before the app is imported. The app reads the address when it starts, so the variable must be set first.
- The migrations run once for the whole test run (`migrated_database`), so the tests use the real schema.
- Each test starts with an empty table, so no test sees another test's rows. Emptying the table is faster than rebuilding the database.

The migration tests use their own empty file, through `monkeypatch`, so they never touch the file the other tests use. `db_query` runs a plain SQL statement, which lets a test check what was actually written.

## 8. Common mistakes
- Forgetting `await session.commit()`, so the change is lost when the request ends.
- Reading an expired attribute after a commit in async code, which fails with `MissingGreenlet`.
- Editing a migration that has already run, so the database and the files disagree. Write a new revision instead.
- A new column with no server default, which fails on any database that already has rows.
- Keeping state in a module-level dict and calling it a database. It is lost on restart, and each process has its own copy.
- Forgetting to import the models in `env.py`, so autogenerate sees no tables and writes an empty migration.

## Exit checklist
- [ ] I can explain the engine, the session and `get_session`, and why `expire_on_commit` is off
- [ ] I can write a model with a Python default and a database default, and say which one an old row gets
- [ ] I can generate a migration with autogenerate, read it, and apply and undo it
- [ ] I can explain why a new column needs a server default, using the `language` example
- [ ] `pytest tests/test_database.py` passes, all 11 tests, and `pytest` passes all 36
