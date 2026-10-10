# Module 11 (FastAPI): Auth

By the end you can hash passwords, issue and check signed tokens, protect routes with a dependency, and test both the allowed and the denied cases. The project is `fastapi/study-api`.

**Before you start:** finish the database lesson (`../11-database/lesson.md`). The users table is a migration, and every login reads a row. Install the new requirements:

```bash
pip install -r requirements.txt
```

This module adds three packages: `pwdlib` with Argon2 for password hashing, `PyJWT` for tokens, and `python-multipart`, which FastAPI needs to read a login form.

**A new setting.** The app now needs a secret key to sign tokens. Set `STUDY_SECRET_KEY` to a random string of at least 32 characters before you run `alembic` or the app. Generate one with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

In PowerShell, set it for the current window with `$env:STUDY_SECRET_KEY = "..."`. In bash, use `export STUDY_SECRET_KEY="..."`. The app refuses to start without the key, on purpose.

Run this module's tests with `pytest tests/test_auth.py`. All 22 should pass when you finish. A bare `pytest` runs the whole suite, 58 tests.

**How to read the examples:** the examples use a made-up notes app, not the Study API.

## 1. Dependencies: functions FastAPI calls for you
A route can declare a parameter with `Depends`. FastAPI calls the function before your route runs, once per request, and passes the result in:

```python
from fastapi import Depends, FastAPI

app = FastAPI()


def pagination(limit: int = 20, offset: int = 0) -> dict:
    return {"limit": min(limit, 100), "offset": offset}


@app.get("/notes")
def list_notes(page: dict = Depends(pagination)):
    return {"page": page}
```

A dependency can read query parameters, headers and the body, just as a route can. It can also depend on other dependencies. That makes it the right place for anything every route needs before it can answer: a database session, the signed-in user, a rate limit.

The rule that makes auth work: if a dependency raises an exception, the route never runs. A dependency that raises `HTTPException(401)` stops the request. Everything in this module follows from that.

**Try it:** add `print("pagination ran")` inside `pagination`, and call `/notes` twice in the docs page. The message prints twice, once for each request.

## 2. Passwords are hashed, not stored
Never store a password, or any reversible form of it. Store a hash: a one-way result that you can check a password against, but cannot turn back into the password. Use a hash built for passwords. A fast hash such as SHA-256 lets an attacker try billions of guesses a second. Argon2 is designed to cost time and memory on every guess. `pwdlib` picks a safe default for you:

```python
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

stored = password_hash.hash("correct horse battery")  # starts with $argon2id$
password_hash.verify("correct horse battery", stored)  # True
password_hash.verify("a wrong guess", stored)  # False
```

The stored string holds the algorithm, its settings and a random salt, so checking needs only that one string. Hashing the same password twice gives two different strings.

Hashing is CPU work, and it takes milliseconds. In an `async def` route, that work blocks the event loop, so no other request is served until it finishes. Python module 12 covers the event loop. Run the hash in a worker thread instead:

```python
from fastapi.concurrency import run_in_threadpool

hashed = await run_in_threadpool(password_hash.hash, payload_password)
```

**Try it:** in a Python shell, time `password_hash.hash("x")` with `time.perf_counter()`. Then work out how long 200 logins at once would block the event loop if each one hashed on the loop thread.

## 3. Tokens: signed, with an expiry
A JWT (JSON Web Token) has three parts separated by dots: a header, a payload and a signature. The header and payload are base64 text, which anyone can decode. So the payload holds the user id and an expiry, and never a password or a secret.

The signature is what matters. The server signs the payload with its secret key. When a request comes back with the token, the server recomputes the signature. If it matches, the server issued this token and nobody changed it. The algorithm here is HS256, which means HMAC with SHA-256: the same secret signs and checks.

```python
import jwt

token = jwt.encode({"sub": "42", "exp": expires_at}, secret_key, algorithm="HS256")
payload = jwt.decode(token, secret_key, algorithms=["HS256"])
```

Three rules:

- `sub` (subject) is the user's id as a string. `exp` (expiry) is when the token stops working. PyJWT checks `exp` for you, and raises `ExpiredSignatureError` once it has passed.
- Always pass `algorithms=` to `decode`. It tells PyJWT which algorithm to accept, so a token cannot choose its own. PyJWT refuses to decode without it.
- The secret key is a setting, `STUDY_SECRET_KEY`. It has no default and must be at least 32 characters, so the app cannot start with a weak or forgotten key. Anyone who has the key can sign any token, so it never goes in the code or the repo. The lifetime, `STUDY_ACCESS_TOKEN_MINUTES`, defaults to 30. A short life limits how long a stolen token works.

A token can outlive its user. A deleted user can still hold an unexpired token, so the server also loads the user from the database on each request (section 5).

**Try it:** create a token with your key in a Python shell. Decode it with `jwt.decode(token, options={"verify_signature": False})` and no key, and read the payload. Then decode it with the wrong key, and read the error. Say what each step proves.

## 4. The users table, and the register and login routes
The users table holds a username, which is unique, and a password hash. It never holds a password. Write the `User` model, then generate the migration from it:

```bash
alembic revision --autogenerate -m "add users"
alembic upgrade head
```

Read the new file before you apply it. It creates one table, and the unique constraint on `username` is what stops two accounts sharing a name.

Three schemas define what goes in and out:

- `UserIn` is the register request: a username of 3 to 50 characters, a password of 8 to 128 characters, and no extra fields.
- `UserOut` is what the API returns. It has the id and the username, and never the hash.
- `Token` is the login reply: `access_token`, and `token_type`, which is `"bearer"`.

**Register.** `POST /auth/register` hashes the password and saves the user. A taken username raises `IntegrityError` from the unique constraint, so the database enforces uniqueness even when two requests race. The route catches the error, rolls back, and answers 409. Checking with a `SELECT` first would leave a gap between the check and the insert.

**Log in.** `POST /auth/token` takes a form, not JSON. `OAuth2PasswordRequestForm` reads `username` and `password` from the form body, which is the standard OAuth2 password flow. The Authorize button in the docs page uses this same route. A successful login returns a token.

A wrong password and an unknown username get the same 401 with the same detail. Otherwise the reply tells an attacker which usernames exist. The 401 also carries `WWW-Authenticate: Bearer`, which tells the client how to authenticate.

**Try it:** register the same username twice in the docs page, and read the 409. Then log in with a wrong password, and then with an unknown username. Compare the two replies.

## 5. Protecting a route with get_current_user
`OAuth2PasswordBearer` reads the `Authorization: Bearer <token>` header. If the header is missing, FastAPI answers 401 before your code runs. The next step is a dependency that turns a valid token into a user:

```python
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(token: str = Depends(oauth2_scheme), session=Depends(get_session)):
    ...  # read the user id from the token, load the user, or raise a 401
```

Any route that takes `user: User = Depends(get_current_user)` is then protected, and it receives the user it needs. The function bodies in `app/security.py` and `app/dependencies.py` are yours to write (TODOs 16 and 18).

Two status codes are easy to mix up:

- **401 Unauthorized** means "I do not know who you are": no token, a bad token, an expired token, or a token for a user who no longer exists.
- **403 Forbidden** means "I know who you are, and you may not do this." Ownership checks answer 403. Some APIs answer 404 instead, so that a caller cannot tell that someone else's resource exists.

**Try it:** open `/docs`, press Authorize, log in, and call `GET /me`. Then press Logout and call it again. Explain both answers. Then call `GET /me/summaries` with the same token, and check that the list holds only your own summaries.

## 6. Dependencies that use dependencies
`get_current_user` depends on two things: the token scheme, and `get_session`. FastAPI resolves the whole tree for each request and calls each function once. If two parts of the same request need `get_session`, they share one session. Dependencies are cached per request by default:

```python
@app.get("/me/summaries")
async def my_summaries(user = Depends(get_current_user), session = Depends(get_session)):
    ...
```

Here `get_current_user` opens the session to load the user, and the route uses the same session for its query. Only one session is created. Pass `use_cache=False` to `Depends` if a dependency has to run again within the same request. That is rare.

**Try it:** add `print("session opened")` at the start of `get_session` in `app/database.py`. Call `GET /me/summaries` with a token, and count the lines printed. Then add a second `Depends(get_session)` parameter to the route, and count again.

## 7. Routes that work with or without a user
Creating a summary works signed in or not. A signed-in request records its owner. An anonymous one records `"anonymous"`. The dependency for this is `get_optional_user`: it returns `None` when there is no token, and the user when there is a valid one.

Here is the trap. A bad token is not the same as no token. Suppose the optional dependency caught the 401 for a forged token and returned `None`. Then the route would save the summary as anonymous, and nobody would notice. The rule: no header gives `None`, and a header that does not check out gives a 401. The test `test_a_bad_token_on_an_open_route_is_refused_and_saves_nothing` checks this rule.

A header that is not `Bearer` counts as no token. That is safe here. It lands on the anonymous path, and it cannot make a request look signed in.

**Try it:** send `POST /summaries` with the header `Authorization: Bearer nope`, using `curl` or your HTTP client, and read the 401. Then send the same request with no header, and compare the owner in the database.

## 8. Tests that replace a dependency
Most tests in `test_auth.py` make a real account, log in, and send the real token. That is the only way to test the rules themselves. A replaced check proves nothing about the check.

For a test that only needs *some* user, a dependency override is simpler. `app.dependency_overrides` maps a dependency to its replacement:

```python
app.dependency_overrides[get_current_user] = lambda: User(id=7, username="tester")
try:
    response = client.get("/me")
finally:
    app.dependency_overrides.clear()
```

The `finally` matters. An override left in place changes every test that runs after it. The override test in `test_auth.py` clears it this way.

**Try it:** in `tests/test_auth.py`, move `test_a_dependency_override_replaces_the_login_in_a_test` above `test_me_without_a_token_is_a_401`, and remove its `finally` block. Run the file. Which test fails, and why? Put the file back the way it was.

## 9. Common mistakes
- Storing a plain password, or a hash from a fast algorithm such as SHA-256 or MD5.
- Logging a password or a token. Logs outlive the request, and anyone who reads them can sign in.
- Trusting a token without loading the user, so a deleted user can still act.
- Calling `jwt.decode` without `algorithms=`, or letting the token choose its algorithm.
- Giving the secret key a default, or a short one. The app should refuse to start.
- Returning the `User` row itself. Without `response_model=UserOut`, the hash goes out with it.
- Catching the 401 in an optional dependency and returning `None`. A forged token then looks like an anonymous request.
- Hashing on the event loop. Use `run_in_threadpool`.

## 10. What this module does not cover
The Study API still has gaps, and you should know them:

- Anyone can delete any summary. `test_basics.py` deletes without a token, and that test has to keep passing for the course. A real app would check the owner before deleting.
- Tokens cannot be revoked. A token works until its `exp`. Real apps add refresh tokens and a way to log out everywhere.
- Login has no rate limit, so a password can be guessed as fast as the server answers.
- A login for an unknown username skips the hash, so its reply comes back sooner. Someone who times the replies can work out which usernames exist. The fix is to run a hash for unknown users too.

## Exit checklist
- [ ] I can explain what `Depends` does, and why a dependency that raises stops the route
- [ ] I can say why passwords use a slow hash, and why the hash runs in a thread
- [ ] I can say what a JWT's payload reveals, and what its signature proves
- [ ] I can protect a route with `get_current_user`, and say when a response is 401 and when it is 403
- [ ] I can explain why a bad token must not become an anonymous request
- [ ] I can override a dependency in a test, and clear the override afterwards
- [ ] `pytest tests/test_auth.py` passes all 22 tests, and `pytest` passes all 58
