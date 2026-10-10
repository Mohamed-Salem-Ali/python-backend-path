# Module 10 (FastAPI): Basics

By the end you can write routes with path, query and body parameters, answer with the right status codes, hide fields with response models, and read the automatic docs. The project for this module is `fastapi/study-api`.

**Before you start:** finish the Python track through module 12 (async and `await`), and module 11 (type hints). FastAPI reads your type hints, so they are the main thing you write. If you know Django REST Framework from module 06 of the Django track, you will recognise most ideas.

**Setup:** from `fastapi/study-api`, install the packages and run the tests:

```bash
pip install -r requirements.txt
pytest
```

Start the server with `uvicorn app.main:app --reload`, then open `http://127.0.0.1:8000/docs`. Stop it with Ctrl+C.

**How to read the examples:** the examples use a made-up `notes` app. It is not part of the Study API. The exercises are the Study API's summaries routes.

## 1. What FastAPI does with your type hints
A FastAPI route is a Python function with type hints. From those hints, FastAPI works out four things for you:

- which URL and HTTP method the function answers (from the decorator)
- how to read each parameter (from the path, the query string, or the JSON body)
- how to check each value, and what to answer when a check fails (422)
- what the documentation says about the route

Run by `uvicorn`, an ASGI server, the app answers each request. Every route that is `async def` runs on the event loop you learned in module 12. Every route that is a plain `def` runs in a pool of threads, which section 8 explains.

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}
```

**Try it:** start the server and call `/health` in the browser. Then open `/docs` and find the same route in the list.

## 2. Routing: one decorator per method
Each HTTP method has a decorator: `@app.get`, `@app.post`, `@app.put`, `@app.delete`. The string is the path.

As an app grows, group the routes in an `APIRouter`. A router takes a prefix and tags. The tags group the routes in the docs. You then add the router to the app with `include_router`:

```python
from fastapi import APIRouter, FastAPI

notes = APIRouter(prefix="/notes", tags=["notes"])


@notes.get("")  # the full path is /notes
def list_notes():
    return []


app = FastAPI()
app.include_router(notes)
```

A route that is defined on a router does nothing until the router is included. If a route you wrote returns 404, check that its router is included.

## 3. Path parameters
A name in braces is a path parameter. Its type hint converts the text from the URL:

```python
@notes.get("/{note_id}")
def get_note(note_id: int):
    return {"id": note_id}
```

`/notes/7` gives `note_id` the integer 7. `/notes/abc` cannot be converted, so FastAPI answers 422 before your code runs. Its body says which parameter failed and why. Without a type hint, the value stays a string.

**Try it:** call `/notes/abc` on the running server, and read the 422 body. Which field does it name?

## 4. Query parameters
A simple parameter that is not in the path is a query parameter. Its default makes it optional. `Query` adds rules, such as a minimum and a maximum:

```python
from fastapi import Query


@notes.get("")
def list_notes(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0)):
    return []
```

`ge` means greater or equal, and `le` means less or equal. A value outside the rule gets the same 422 as a bad path value. To make a parameter optional with no default, use `str | None = None`.

**Try it:** call `/notes?limit=0`, then `/notes?limit=50`. Read both answers.

## 5. The request body
A parameter whose type is a Pydantic model is read from the JSON body:

```python
from pydantic import BaseModel


class NoteIn(BaseModel):
    title: str
    body: str = ""


@notes.post("")
def create_note(payload: NoteIn):
    return payload
```

A field with no default is required. A body that lacks it gets a 422 whose `detail` list names the field, under `loc`. The next module in this track, on Pydantic, covers the rules you can put on fields.

**Try it:** send a POST with only `title`, then with nothing. Compare the two 422 bodies.

## 6. Response models hide fields
The data you store often holds fields the client must not see, such as an owner id or a password hash. A response model decides what leaves the server:

```python
from pydantic import BaseModel


class NoteOut(BaseModel):
    id: int
    title: str


@notes.get("/{note_id}", response_model=NoteOut)
def get_note(note_id: int):
    return {"id": note_id, "title": "hello", "owner": "sara"}  # owner is not sent
```

FastAPI keeps only the fields that `NoteOut` lists. The function can return a dict with more fields, and the reply still has only `id` and `title`. The model also documents the reply, so the docs show it.

**Try it:** remove `response_model=NoteOut` from the route, call it, and see the `owner` field appear. Put it back.

## 7. Status codes and errors
The decorator sets the status a route answers with. Use the status that matches what happened:

| Situation | Status | How |
|---|---|---|
| Read or update worked | 200 | the default |
| Something was created | 201 | `status_code=201` on the decorator |
| Something was deleted, with nothing to send back | 204 | `status_code=204`, and return nothing |
| The thing asked for does not exist | 404 | `raise HTTPException(status_code=404, detail="...")` |
| The request is badly formed | 422 | FastAPI answers this for you |

`HTTPException` stops the route and sends `{"detail": ...}` with the status you set. A 204 sends no body, so a client must not read one.

**Try it:** the Study API's `test_delete_answers_204_with_no_body_then_404` checks both rules. Read it, and find the line that checks there is no body.

## 8. `def` or `async def`
FastAPI runs a plain `def` route in a thread pool, so a blocking call inside it only blocks its own thread. An `async def` route runs on the event loop with every other request. That is faster for work that waits on the network, if the work uses `await`.

The rule from module 12 applies: a blocking call inside `async def` freezes the event loop, and every other request waits. `time.sleep`, a synchronous database driver, or a slow file read are all blocking calls. If the route has to call one, use a plain `def`, or move the call to a thread with `asyncio.to_thread`.

**Try it:** write two `async def` routes that call `time.sleep(2)`. Start the server, and call both at once from two terminals. The second one waits. Replace `time.sleep` with `await asyncio.sleep(2)` and try again.

## 9. The docs come from the code
`/docs` shows an interactive page for every route. `/openapi.json` is the machine-readable description behind it. Both are built from the decorators, the type hints and the response models. A route that lacks a `status_code=201` documents a 200, which is why the Study API's tests check the spec too.

## 10. Testing a route
`TestClient` from `fastapi.testclient` sends requests to your app in the same process, with no server:

```python
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
response = client.post("/notes", json={"title": "hi"})
assert response.status_code == 201
```

The Study API's `conftest.py` makes a `client` fixture and empties the store before each test, so no test sees another test's data.

## Exit checklist
- [ ] I can write a route with a path parameter, a query parameter and a body, and say which is which
- [ ] I can name the status codes for create, delete, not found, and a bad request
- [ ] I can explain why a response model is needed when the stored data has a secret field
- [ ] I can say what goes wrong with `time.sleep` inside `async def`
- [ ] `pytest` passes in `fastapi/study-api`, all 14 tests

## Common mistakes
- Forgetting `include_router`, so the routes do not exist.
- Returning a stored record without a response model, so secret fields leave the server.
- Leaving out `status_code=201`, so a create answers 200.
- A path parameter without a type hint, so the value arrives as a string.
- A blocking call inside `async def`.
