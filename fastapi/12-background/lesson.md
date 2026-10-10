# Module 12 (FastAPI): Background work and testing

By the end you can queue slow work to run after a response, give that work its own database session, replace a dependency in a test, and write async tests. The project is `fastapi/study-api`.

**Before you start:** finish the auth lesson (`../11-auth/lesson.md`), which covers dependencies and overrides, and the database lesson (`../11-database/lesson.md`). Install the requirements again. This module adds `anyio`, whose pytest plugin runs the async tests:

```bash
pip install -r requirements.txt
```

Run this module's tests with `pytest tests/test_background.py`. All 18 should pass when you finish. A bare `pytest` runs all 76 tests.

**How to read the examples:** the examples use a made-up notes app, not the Study API.

## 1. Background work runs after the response
A request should answer quickly. Work that is slow, and that the reply does not depend on, can run after the response is sent. `BackgroundTasks` does this. A route adds a function to it, and the function runs after the response goes out, in the same process:

```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def send_receipt(email: str) -> None: ...  # slow: calls an email service


@app.post("/orders", status_code=201)
def create_order(email: str, background: BackgroundTasks):
    background.add_task(send_receipt, email)
    return {"status": "created"}
```

A plain `def` function runs in a worker thread, so it does not block the event loop. An `async def` function runs on the loop, so it must not call blocking code.

`BackgroundTasks` is the simplest option, and it has limits. The work lives in the web process: a restart loses it, nothing retries it, and nothing records that it ran. Section 9 covers when to use a real queue.

**Try it:** add `time.sleep(5)` inside `send_receipt`, and call `/orders` from the docs page. The reply comes back at once, and the sleep happens after it.

## 2. A route that queues the work
The Study API queues flashcard making for a summary. `POST /summaries/{id}/flashcards` answers **202 Accepted**. The status code means the work was accepted, not that it is done. The reply holds the status `"queued"` and the summary id.

```python
from fastapi import BackgroundTasks, Depends, HTTPException


@app.post("/notes/{note_id}/digest", status_code=202)
async def queue_digest(
    note_id: int,
    background: BackgroundTasks,
    session: AsyncSession = Depends(get_session),
):
    if await session.get(Note, note_id) is None:
        raise HTTPException(status_code=404, detail="note not found")
    background.add_task(write_digest, note_id)
    return {"status": "queued", "note_id": note_id}
```

The route checks that the summary exists before it queues anything, so a missing summary is a 404 and creates no job. The matching `GET` route lists the cards, and it returns an empty list until the job has written them.

**Try it:** create a summary, call the queue route, and read the 202 reply. Then call the list route straight after. On a running server the list can still be empty for a moment. In the tests it never is, as section 7 explains. Say why.

## 3. The job gets its own session
A request's session belongs to the request. The `get_session` dependency opens it for the request, and the job must not reuse it. The job opens its own session from the sessionmaker in `database.py`:

```python
from app.database import SessionLocal


async def write_digest(note_id: int) -> None:
    async with SessionLocal() as session:
        note = await session.get(Note, note_id)
        if note is None:
            return
        ...  # make the digest, add the rows
        await session.commit()
```

Two more rules follow from this:

- Pass the job ids, not ORM objects. An object loaded in the request is attached to the request's session. The job receives the id and loads the row itself.
- The job commits its own work. Nothing else commits for it, so a job without `commit()` saves nothing.

**Try it:** explain why `write_flashcards` receives `summary_id` and not the `Summary` object. Then check the function's signature in `app/services.py`.

## 4. A table that points at summaries: foreign keys and cascades
A flashcard belongs to one summary. The model stores the summary's id in a foreign key, and the key says that deleting the summary deletes its cards:

```python
summary_id: Mapped[int] = mapped_column(ForeignKey("summaries.id", ondelete="CASCADE"))
```

SQLite ignores foreign keys unless each connection switches them on with `PRAGMA foreign_keys=ON`. Without that, the `ondelete` clause does nothing, and the cards are left pointing at a summary that no longer exists. The engine in `database.py` runs the PRAGMA on every new connection. It does this only for SQLite, because other databases enforce foreign keys without it.

Then generate the migration, and read it before you apply it:

```bash
alembic revision --autogenerate -m "add flashcards"
alembic upgrade head
```

The generated `ForeignKeyConstraint` line must end in `ondelete='CASCADE'`. The test `test_the_cards_reference_the_summary_with_a_cascade` checks the schema, and `test_the_migrations_match_the_models` checks that the model and the migration agree.

**Try it:** remove the `cursor.execute("PRAGMA foreign_keys=ON")` line from `database.py`, and run `pytest tests/test_background.py -k deleting`. Read the failure: the cards are still there. Put the line back.

## 5. The maker is a dependency
The job needs a function that takes a summary's text and returns `(front, back)` pairs. Today that is the stand-in in `app/flashcards.py`. Later it will be a model call, which is slow and needs a key. The route does not import the function. It gets it from a dependency, and passes it to the job:

```python
def get_digest_writer():
    return write_digest_with_model


@app.post("/notes/{note_id}/digest", status_code=202)
async def queue_digest(
    note_id: int,
    background: BackgroundTasks,
    writer=Depends(get_digest_writer),
    session: AsyncSession = Depends(get_session),
):
    ...
    background.add_task(run_digest, note_id, writer)
```

This buys two things. A test replaces the function with a fake, using the override from the auth lesson, and it can check what the job received. And the job only sees text in and pairs out, so changing the implementation changes nothing else.

**Try it:** in `app/routers/summaries.py`, change `Depends(get_flashcard_maker)` to call `make_flashcards()` directly. Run `pytest tests/test_background.py -k dependency`. Which test fails, and why? Put the code back.

## 6. When the work fails, and when it runs twice
Nobody waits on a background job, so nobody sees its errors unless they reach the log. The job catches an error from the maker, logs it with `logger.exception`, which keeps the traceback, and returns. The maker runs before anything is deleted, so the old cards stay in place.

A job can also run twice, because a client queued it twice. The job deletes the old cards and adds the new ones in one transaction. A second queue therefore replaces the cards and does not double them. A failed run also deletes nothing, because the delete comes after the maker has succeeded.

**Try it:** remove the `try` and `except` around the maker, and run `pytest tests/test_background.py -k keeps`. Read the error. Put the code back, then remove the `delete(...)` line, and run `-k replaces`.

## 7. Testing background work
Two facts about the test client shape these tests:

- `TestClient` returns only after the whole app call has finished, background tasks included. So after `client.post(...)`, the cards exist. This keeps route tests simple.
- That same fact hides the real timing. In production the client gets the 202 before the job runs. Do not write a test that depends on the gap, and test the job itself, by calling it.

For the job, the test calls `write_flashcards` directly and awaits it. An async test needs a plugin to run the coroutine. The project uses `anyio`, which is installed with Starlette, and a test marked with `@pytest.mark.anyio` runs on the asyncio event loop:

```python
import httpx2
import pytest


@pytest.mark.anyio
async def test_the_job_saves_the_cards(db_query):
    summary_id = insert_summary(db_query)
    await write_flashcards(summary_id, lambda text: [("Q", "A")])
    assert db_query("SELECT front, back FROM flashcards") == [("Q", "A")]
```

To call the app from an async test, use `httpx2.AsyncClient` with an `ASGITransport`. The client runs the app on the test's own event loop, so you can `await` each request:

```python
async with httpx2.AsyncClient(
    transport=httpx2.ASGITransport(app=app), base_url="http://test"
) as client:
    response = await client.get("/health")
```

The fixtures stay synchronous in this project. Only the test bodies are async. The package is `httpx2`, which the project pins. A plain `import httpx` is a different library, and it is not installed by the requirements.

**Try it:** in `tests/test_background.py`, delete the `@pytest.mark.anyio` line above `test_the_job_saves_the_cards_its_maker_returns`, and run `pytest tests/test_background.py -k saves`. Read what pytest reports about the coroutine. Put the line back.

## 8. Common mistakes
- Passing a request-scoped object, such as a loaded `Summary`, into the job. Pass the id.
- Using the request's session in the job. The job opens its own.
- Forgetting `await session.commit()` in the job. Nothing is saved.
- Running a slow sync maker on the event loop from an async job. Use `run_in_threadpool`.
- Catching an error in the job and saying nothing. Log it, because no one else sees it.
- Writing a test that depends on the gap between the 202 and the job.
- Leaving out the PRAGMA, so the cascade silently does nothing.
- Using `BackgroundTasks` for work that must not be lost.

## 9. Real queues, and what this module does not cover
`BackgroundTasks` fits work that is short, can be lost without harm, and needs no record. Reach for a real queue when the work is long, must survive a restart, needs retries, or should run on another machine. The queue keeps jobs outside the web process, and a separate worker picks them up. The Django track's Celery module (`../../django/10-background-tasks/lesson.md`) covers one such queue. ARQ and RQ are others.

This module does not cover:

- A status endpoint. A client cannot ask whether the job finished. A real API returns a job id, and a route reports its status.
- Retries. A failed maker is logged, and nothing tries again.
- Two jobs for the same summary running at once. Their delete and insert can interleave. A real queue, or a lock, prevents that.
- A slow maker. The job opens its session before it calls the maker, so the connection is held while the maker runs. A real version loads the text, closes the session, runs the maker, then opens a new session to write.

## Exit checklist
- [ ] I can explain when `BackgroundTasks` runs, and what it cannot do: survive a restart, or retry
- [ ] I can return 202 and say what it promises: the work was accepted, not finished
- [ ] I can give a background job its own session, and pass it ids rather than objects
- [ ] I can write a foreign key with `ondelete="CASCADE"`, and say why SQLite needs the PRAGMA
- [ ] I can replace a dependency in a test, and say what the test client does before it returns
- [ ] I can write an async test with the `anyio` marker, and an async client with `httpx2`
- [ ] `pytest tests/test_background.py` passes all 18 tests, and `pytest` passes all 76
