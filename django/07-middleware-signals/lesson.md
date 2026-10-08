# Module 07 (Django): Middleware and signals

By the end you can write middleware that runs around every request, order it in settings, write a signal receiver that reacts to a model event, connect it so it actually runs, and say when a signal is the wrong tool.

**Before you start:** finish modules 02 to 06. The audit log uses the `Payment` and `Member` models.

**How to read the examples:** the code here uses the made-up library app from module 04: `Book`, `Reader` and `Review`. None of it is part of Gameya. Learn the pattern here, then apply it to Gameya in `circles/middleware.py`, `circles/signals.py` and `circles/apps.py`.

## 1. Middleware wraps every request
Django runs each request through a chain of middleware before it reaches the view, then runs the response back through the same chain. Each middleware is a layer around the next one, like the layers of an onion:

```text
request  ->  SecurityMiddleware  ->  SessionMiddleware  ->  ...  ->  view
response <-  SecurityMiddleware  <-  SessionMiddleware  <-  ...  <-  view
```

The order is the order in `MIDDLEWARE` in `config/settings.py`. The first entry is the outermost layer: it sees the request first and the response last. A middleware can read or change the request, call the rest of the chain, and then read or change the response.

## 2. A middleware is a class with two methods
Django creates one instance when the server starts. The instance keeps a reference to the next layer, `get_response`, and is called once for each request:

```python
import time

class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started = time.perf_counter()        # the request phase: before the view
        response = self.get_response(request)
        elapsed_ms = (time.perf_counter() - started) * 1000
        response["X-Response-Time-Ms"] = f"{elapsed_ms:.1f}"   # the response phase
        return response
```

Everything before `get_response(request)` runs on the way in. Everything after it runs on the way out, when the response exists. A middleware that sets a header must do it after the call, because the response does not exist before it.

## 3. Short-circuit: answer without calling the view
A middleware does not have to call `get_response`. If it returns a response itself, the rest of the chain and the view never run. A closed-library switch is one example:

```python
from django.conf import settings
from django.http import HttpResponse

class StocktakeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if getattr(settings, "LIBRARY_CLOSED", False):
            return HttpResponse("Closed for stocktake.", status=503)
        return self.get_response(request)
```

Use this with care. A middleware that answers too early skips the layers after it, including authentication and sessions.

## 4. Order matters
Some middleware needs another one to run first. `AuthenticationMiddleware` sets `request.user`, so any middleware that reads `request.user` must come after it. `SessionMiddleware` must come before `AuthenticationMiddleware`, because the user is found in the session. Put your own middleware at the top of the list if it must see every request, and below the layers it depends on if it reads what they add.

## 5. Signals: a sender tells the world something happened
A signal is a message that Django sends when something happens to a model. The built-in ones include:

| Signal | When it is sent | Arguments |
|---|---|---|
| `pre_save` | just before `save()` writes the row | `sender`, `instance`, `raw` |
| `post_save` | just after the row is written | `sender`, `instance`, `created`, `raw` |
| `pre_delete` | just before a row is deleted | `sender`, `instance` |
| `post_delete` | just after a row is deleted | `sender`, `instance` |

`created` exists only on `post_save`. Before the write, Django does not yet know whether it will insert a new row or update an existing one, so `pre_save` cannot tell you.

A **receiver** is a function that listens for a signal. Use the `receiver` decorator, and name the model with `sender`:

```python
import logging
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Review)
def log_new_review(sender, instance, created, **kwargs):
    if created:
        logger.info("new review: %s stars on book %s", instance.stars, instance.book_id)
```

Every receiver takes `sender` and `**kwargs`, so a new argument that Django adds later does not break it. Model signals also pass `instance`, the row itself. The `**kwargs` is required, because Django passes extra arguments that a receiver may not use.

## 6. Connect your receivers, or nothing runs
Defining a receiver is not enough. The module that holds it must be imported when the app starts. The usual place is the app's `ready()` method, which Django calls once at start-up:

```python
from django.apps import AppConfig

class LibraryConfig(AppConfig):
    name = "library"

    def ready(self):
        from . import signals  # noqa: F401  (importing connects the receivers)
```

Do not import the module at the top of `apps.py`. At that point the app registry is not ready, and the import fails with `AppRegistryNotReady`. Inside `ready()`, the registry is ready and the import works.

If a receiver silently does nothing, check this first. The most common signal bug is a receiver that was written, tested by hand, and never imported.

## 7. Where the receiver runs
`post_save` runs after the row has been written to the database. Whether a receiver's error can undo that row depends on the transaction:

- **In autocommit mode** (Django's default, with no surrounding transaction), the row is committed before `post_save` runs. If a receiver raises, `save()` raises that error, but the row stays in the database.
- **Inside a transaction** (a `transaction.atomic()` block, `ATOMIC_REQUESTS`, or a `TestCase`), the same error rolls back the row as well.

Delete works differently. Django runs `pre_delete`, the `DELETE` statements and `post_delete` inside one transaction of its own. So a `post_delete` receiver that raises undoes the delete, even outside `atomic()`.

If the database rejects the row, for example because of a unique constraint, `save()` raises before `post_save` is sent. A receiver never sees a row the database refused.

Deleting follows its own rule for related rows. Deleting a book also deletes its reviews. If a receiver is connected for `Review`, each review is loaded and sends its own `post_delete`. Without a receiver, Django can delete the rows without loading them.

## 8. When not to use a signal
Signals are easy to add, and easy to misuse. They hide the flow of the code: someone who reads `book.save()` cannot see that it also sends an email. Prefer a plain method call when the action is part of the model's job. Use a signal when the action belongs to another part of the program, such as a log or a notification, and the model does not need to know about it.

They also do not run for everything:
- `bulk_create()` and `bulk_update()` do not send `post_save`.
- `QuerySet.update()` does not send any signal.
- Raw SQL sends nothing.
- Loading fixtures sends `post_save` with `raw=True`. Rows that this row refers to may not be loaded yet, so a receiver should usually do nothing when `raw` is `True`.

If a rule must hold for every row, however it is written, use a database constraint (module 02), not a signal.

Finally, a signal is a poor place for a rule that decides whether a save is allowed. Validation belongs in `clean()` or in a form (module 03), where the user sees the error.

## 9. Testing middleware and signals
Test a receiver the way it runs: save a real row, then check the side effect. A test that calls the receiver function directly would pass even if the receiver were never connected.

Test middleware in two ways. Through the client, the test sees the header on a real response. Directly, `RequestFactory` builds a request, and the test calls the middleware with a small view, so it can check what the middleware stores on the request:

```python
from django.http import HttpResponse
from django.test import RequestFactory

def view(request):
    return HttpResponse("ok")

response = TimingMiddleware(view)(RequestFactory().get("/"))
assert "X-Response-Time-Ms" in response
```

## 10. Habits
- Keep middleware small. It runs on every request, including the ones that fail.
- Put the order in the settings file, and comment on any order that matters.
- Use `**kwargs` in every receiver.
- Import receivers in `ready()`, and check that they fire with a test.
- Choose a plain method for core rules, and a signal for side effects.

## Check your understanding
1. In what order do `MIDDLEWARE` entries see a request, and in what order do they see the response?
2. A middleware tries to set a response header before it calls `get_response`. What goes wrong, and why?
3. Why must `AuthenticationMiddleware` come before a middleware that reads `request.user`?
4. Why does `post_save` receive `created`, and why can a `pre_save` receiver not tell whether a row is new?
5. A receiver is written and tested by hand, but the log never changes when a row is saved. What is the most likely cause?
6. A rule says a reader cannot review the same book twice. Why is a `post_save` receiver the wrong place for it?
7. A `bulk_create()` of 500 reviews runs. Which receivers run for those rows?

## Do the exercises
1. **Middleware.** Write `RequestIdMiddleware` in `circles/middleware.py` (TODO 23). Read the `X-Request-ID` header, keep a valid id, make a new one otherwise, store it on the request, and set it on the response.
2. **Settings.** Add `"circles.middleware.RequestIdMiddleware"` as the first entry of `MIDDLEWARE` (TODO 27). Then run `python manage.py test circles.tests.test_middleware_signals.RequestIdMiddlewareTests`. Its eight tests should pass.

   Add the setting only after the class exists. Once it is listed, Django imports the class for every request. A missing class then breaks every test that makes a request, in every module.
3. **Model.** Write `AuditEntry` in `circles/models.py` (TODO 26), then run `python manage.py makemigrations circles` and `python manage.py migrate`. Run `python manage.py test circles.tests.test_models` to check that the models and migrations still agree.
4. **Receivers.** Write the three receivers in `circles/signals.py` (TODO 24). Do not import `AuditEntry` until step 3 is done.
5. **Connect them.** Add `ready()` to `CirclesConfig` in `circles/apps.py` (TODO 25). Without it, the audit tests fail with no entry written.
6. **Run the module.** Run `python manage.py test circles.tests.test_middleware_signals`. Stop when all 16 tests pass.
7. **Check it by hand.** Run `python manage.py runserver` in a second terminal, then in PowerShell:
   ```powershell
   curl.exe -i http://127.0.0.1:8000/api/
   curl.exe -i -H "X-Request-ID: my-test-1" http://127.0.0.1:8000/api/
   ```
   Look for `X-Request-ID` in the output. The second command sends its own id, and the same id should come back.

**Stretch (not tested):** add a middleware that counts the requests since the server started, and puts the count in a header. Explain why a count kept in a global variable is not safe with several server processes, and what you would use instead.

**Project step:** every response now carries a request id, and every new payment and every payment or member that is deleted is recorded in the audit log. Module 08 (testing in Django) gives the project a full test suite.

**Done when:** all of `test_middleware_signals` passes, and you can explain why a receiver that was never imported does nothing.
