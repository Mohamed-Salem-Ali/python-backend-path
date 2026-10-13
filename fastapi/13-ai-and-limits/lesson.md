# Module 13 (FastAPI): A real model, and rate limits

By the end you can call a model's HTTP API from FastAPI without blocking the event loop, keep the key out of code, logs and tests, turn every way the call can fail into one clear answer, choose the model or the stand-in with a setting, and limit how often one caller can use a route. The project is `fastapi/study-api`.

**Before you start:** finish the Docker lesson (`../12-docker/lesson.md`). This is a bonus module for after week 12. It finishes what the plan calls the AI wrapper API. Nothing here needs a new package: `httpx2` is already in `requirements.txt`, because the tests use it.

**You do not need an API key.** The app keeps the stand-ins from earlier modules as the default, and every test fakes the model. Section 10 shows how to switch on a real model when you want to see it work.

Run this module's tests with `pytest tests/test_ai.py`. All 29 should pass when you finish. A bare `pytest` runs the whole suite, 117 tests.

**How to read the examples:** the examples use a made-up notes app, not the Study API. The weather API in section 2 is made up too.

## 1. Settings for a model
A model call needs four values that change between a laptop and a server: which provider to use, the key, the model name and how long to wait. They are settings, read from the environment like the others:

```python
from typing import Literal

from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="NOTES_")
    translator: Literal["off", "remote"] = "off"
    translator_key: SecretStr | None = None

    @model_validator(mode="after")
    def remote_needs_a_key(self):
        if self.translator == "remote" and self.translator_key is None:
            raise ValueError("NOTES_TRANSLATOR_KEY is required when NOTES_TRANSLATOR is remote")
        return self
```

Three ideas are new here:

- **`Literal`** limits a setting to a few named values. A typo such as `gemeni` is refused when the app starts, not on the first request.
- **`SecretStr`** wraps the key. Printed, logged or dumped, it shows `**********`. You read the real value only where you send it, with `get_secret_value()`. A key that leaks into a log or an error page is a leaked key.
- **`model_validator(mode="after")`** checks fields together, after each one has passed its own rules. A remote provider without a key is a setup mistake, so the app refuses to start.

The safe default matters. With no settings at all, the Study API uses the stand-ins: no network, no cost, no key.

**Try it:** in a Python shell, make a `Settings` with a fake key and `print()` it. Then call `.model_dump()` and print that. Find the key in neither. Then call `.translator_key.get_secret_value()`.

## 2. Calling an HTTP API with httpx2
Most model providers, Gemini among them, are an HTTP API: you send JSON with `POST`, and JSON comes back. `httpx2` sends it. With a `Client` in a `with` block, the connection closes when the block ends:

```python
import httpx2

with httpx2.Client(timeout=10) as client:
    response = client.post(
        "https://weather.example/v1/forecast",
        json={"city": "Cairo", "days": 3},
        headers={"x-api-key": key.get_secret_value()},
    )
    response.raise_for_status()
    data = response.json()
```

- **The timeout is not optional.** Without one, a call can hang for minutes, and the request that made it hangs with it. Choose a timeout that is shorter than your users' patience.
- **The key goes in a header.** An address ends up in proxy logs, browser history and error reports. A header does not. Gemini reads it from the `x-goog-api-key` header.
- **`raise_for_status()`** raises for any 4xx or 5xx status. Without it, a 503 page is read as if it were an answer.

Gemini's address names the model: `.../v1beta/models/<model>:generateContent`. The body holds the prompt in `contents`, and the answer comes back in `candidates[0].content.parts`, a list of parts, each with some text. Some models also send parts marked `"thought": true`, which hold their reasoning, not the answer. Leave those out. A model can also spend a small token budget on that reasoning and have nothing left for the answer, so `maxOutputTokens` stays at 1024 or more.

**Try it:** read `GEMINI_URL` in `app/ai.py` and the TODO above `generate`. Write down, on paper, the JSON body you will send for the prompt "Say hi", before you write any code.

## 3. When the call fails
A call over the network can fail in more ways than a function call can:

| What went wrong | What httpx2 does | Example |
|---|---|---|
| No answer in time | raises `httpx2.TimeoutException` | the model is overloaded |
| No connection | raises `httpx2.ConnectError` | DNS failure, the network is down |
| An error status | `raise_for_status()` raises `httpx2.HTTPStatusError` | 401 bad key, 429 quota, 503 busy |
| A 200 with an odd body | nothing: your code raises `KeyError`, `IndexError` or `TypeError` | the API changed, or the answer is empty |

All three exceptions above derive from `httpx2.HTTPError`. The route should not need to know any of this. So `generate` catches all of these and raises one exception of its own, `ModelError`, with the original attached by `raise ... from error`. The route then has one thing to handle.

What the client sees is a **502 Bad Gateway**. A 502 says the server is working, but something it depends on gave a bad answer. A 500 says your own code broke. The difference tells whoever is on call where to look first.

Do not retry inside the request. Each retry adds the whole timeout to the user's wait. Retries belong in background work, where nobody is waiting (the background work lesson, section 6).

**Try it:** for each row of the table, name the test in `tests/test_ai.py` that covers it. One row has no test of its own. Find it, and write that test in a scratch file: a handler that raises `httpx2.ConnectError`, as the timeout test raises `httpx2.ReadTimeout`.

## 4. Prompts, and answers you cannot trust
A prompt is a request in plain words, and a model follows it most of the time. So the code checks what comes back, and does not just hope:

- **Length.** "At most 50 words" is a request, not a rule. The route cuts the answer with `fit_words`, so the summary never breaks the limit the client asked for. The stand-in already keeps to it, so cutting changes nothing for it.
- **Shape.** For flashcards the code needs a list of pairs, not prose. Gemini can be told to answer in JSON (`"responseMimeType": "application/json"` in `generationConfig`). Even then, read the answer with `json.loads` and check every object for `front` and `back`. Anything else is a `ModelError`.
- **Content.** The text a user sends goes into the prompt, so a user can write "ignore the instructions above". Never give the model's answer more power than the user had: here it is only stored text, so the worst case is a bad summary.

```python
def parse_tags(answer: str) -> list[str]:
    try:
        tags = json.loads(answer)
    except ValueError as error:
        raise ModelError("the tags were not JSON") from error
    if not isinstance(tags, list) or not all(isinstance(tag, str) for tag in tags):
        raise ModelError("the tags were not a list of text")
    return tags
```

**Try it:** list three ways a model's flashcard answer could be wrong, then find the test that covers each one. If a way has no test, write the test you would add.

## 5. The maker is a dependency
The background work lesson made the flashcard maker a dependency, so a test could replace it. This module does the same for the summarizer, and lets the settings choose:

```python
def get_translator():
    settings = get_settings()
    if settings.translator == "off":
        return keep_the_text
    return remote_translator(settings)
```

The route asks for `translator=Depends(get_translator)` and never learns which one it got. Tests replace it with `app.dependency_overrides`, so they never touch the network. Both makers have the same shape as the stand-ins (text in, text or pairs out), so nothing else changes. The flashcard job from module 12 runs the Gemini maker without a single change.

The summarizer runs while the client waits, inside an `async def` route, and a model call waits on the network for a second or more. Called directly, it would hold the event loop, and every other request would wait too. Call it with `run_in_threadpool`, as login does with the password hash.

**Try it:** the test `test_the_summarizer_runs_in_a_worker_thread_not_on_the_event_loop` uses the async client, not the `TestClient`. Read its comment, then explain why a `TestClient` test could not tell the two versions apart.

## 6. Rate limiting: a sliding window
A model call costs money or quota, and a login answer lets someone test a password. Both need a limit on how often one caller may ask. The rule here is "at most N requests in any 60 seconds", and the limiter keeps, for each caller, the times of their recent requests:

```text
limit 2, window 60 s
t=0   hit -> allowed      times: [0]
t=10  hit -> allowed      times: [0, 10]
t=15  hit -> refused      wait 60 - (15 - 0) = 45 s
t=60  hit -> allowed      0 has left the window; times: [10, 60]
```

Before counting, drop the times that are a full window old or older. A refused request is not recorded, so asking again and again does not push the wait further away. The wait is how long until the oldest time leaves the window.

The limiter reads the time from a `clock` you pass in, `time.monotonic` by default. A test passes a clock it moves by hand, so it checks a 60-second window without waiting 60 seconds. `monotonic` and not `time.time`, because the wall clock can jump when the computer syncs its time, and a window measured with it can go wrong.

**Try it:** extend the table above by hand to t=65 and t=70, with the limit still 2. Then check your answers against your limiter in a Python shell, with a clock you move by hand.

## 7. A limit as a dependency
The limit runs before the route, so it is a dependency: if it raises, the route never runs. Two choices shape it:

- **Who is the caller?** A signed-in user is their user id; their budget follows them across networks. Anyone else is their IP address (`request.client.host`). The key also names the route, so logins and summaries count separately.
- **What is the answer?** `429 Too Many Requests`, with a `Retry-After` header that says how many whole seconds to wait. Round up: a client that waits the rounded-down number is refused again.

```python
async def rate_limit(request: Request, limiter=Depends(get_rate_limiter)):
    wait = limiter.hit(f"{request.url.path} ip:{request.client.host}")
    if wait is not None:
        raise HTTPException(429, detail="too many requests", headers={"Retry-After": "30"})
```

That sketch hard-codes the wait and ignores signed-in users; yours must not. Attach it with `dependencies=[Depends(rate_limit)]` on the route's decorator. That is the form for a dependency whose return value the route does not need. In the Study API it goes on creating a summary, which calls the model, and on login. Each `hit` counts, so a wrong password counts as much as a right one.

`get_rate_limiter()` returns the same limiter on every call, because counts kept in a new limiter for each request would always be zero. `functools.cache` builds it once. The tests replace it with a limiter of their own, and the suite sets `STUDY_RATE_LIMIT_PER_MINUTE=0` in `tests/conftest.py`, so the other 88 tests are not refused.

**Try it:** run the server, then send `POST /auth/token` with a wrong password eleven times in under a minute. Read the last response's status and its `Retry-After` header.

## 8. Limits with more than one process
The limiter keeps its counts in the memory of one process. That breaks in three ways:

- **More processes.** With four Uvicorn workers, or two containers, each has its own counts, so a caller gets four times the limit. Shared counts live in a shared store, usually Redis, with a key per caller that expires after the window.
- **A restart** clears every count.
- **A proxy in front.** Behind a load balancer, `request.client.host` is the proxy's address, so every caller shares one budget. Uvicorn's `--proxy-headers` and `--forwarded-allow-ips` options read the real address from the proxy's header. Only trust that header from your own proxy, because anyone can send it.

For a real service, add one more limit: a daily cap on the model calls of the whole app, so a busy day or a bug cannot run up a bill. The provider's own quota is a last line, not a plan.

## 9. Testing without the network
A test that calls a real model is slow, costs quota, fails when the network does, and gets a different answer each time. These tests never do it:

- **The client** is tested with `httpx2.MockTransport`. You give it a function that receives each request and returns a response. The test can read what the code sent (the address, the headers, the body) and decide what comes back: a good answer, a 503 or a timeout.
- **The route** is tested with a dependency override, as in module 12.
- **The limiter** is tested with a clock the test moves by hand.

```python
def handle(request):
    assert request.headers["x-api-key"] == "test-key"
    return httpx2.Response(200, json={"forecast": "sunny"})


transport = httpx2.MockTransport(handle)
```

`generate` takes `transport=None`. The app passes nothing, which means the real network; the tests pass a `MockTransport`.

**Try it:** write a test of your own for `generate`: a handler that returns status 200 with the body `{"candidates": [{"content": {}}]}`. Which exception reaches the test, and which line of your code turned it into a `ModelError`?

## 10. Running it for real
To see a real model answer, get a free API key from Google AI Studio, then set three variables in the terminal where you start the server:

```bash
export STUDY_AI_PROVIDER=gemini
export STUDY_AI_API_KEY="paste-your-key-here"
uvicorn app.main:app --reload
```

In PowerShell, use `$env:STUDY_AI_PROVIDER = "gemini"` and the same for the key. Create a summary and queue its flashcards from the docs page. `STUDY_AI_MODEL` changes the model. The default, `gemini-3.5-flash-lite`, is quick and has a generous free quota; model names change, so check the list in AI Studio if you get a 404.

Rules for the key: it lives in the environment or the host's secret settings, never in the code, the repo, the Dockerfile or a test. If a key ever lands in a commit, revoke it in AI Studio and make a new one. Deleting the commit is not enough, because the old commit can still be fetched. Run `pytest` with the provider unset: the tests do not need a key, and they must not use yours.

## 11. Common mistakes
- No timeout on the call, so one slow answer holds a request open for minutes.
- The key in the address, a log line, a test or the Dockerfile.
- Calling the model on the event loop, so every other request waits for it.
- Letting an httpx2 exception escape, so the client gets a 500 and a traceback in the logs instead of a 502.
- Trusting the model to keep to the word limit, or to answer in valid JSON.
- Retrying inside the request, so a slow model makes the user wait for several timeouts.
- A new limiter for each request, so every count starts at zero.
- Limiting by IP behind a proxy, so every user shares one budget.
- Tests that call the real model.

## Exit checklist
- [ ] I can explain why the key is a `SecretStr`, and where it may and may not appear
- [ ] I can list the ways a model call fails, and say why they all become one `ModelError` and a 502
- [ ] I can explain why the summarizer runs with `run_in_threadpool`
- [ ] I can say why the route cuts the model's answer and checks its JSON, instead of trusting the prompt
- [ ] I can trace a sliding window by hand, and say what `Retry-After` should be
- [ ] I can say why a limiter kept in memory breaks with several processes or behind a proxy
- [ ] I can test an HTTP client with `MockTransport`, and a limiter with a clock I control
- [ ] `pytest tests/test_ai.py` passes all 29 tests, and `pytest` passes all 117
