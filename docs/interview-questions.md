# Interview question bank

Use this bank on Day 6 of each week, as the [12-week plan](12-week-plan.md) says. Pick two or three questions from the modules you finished that week, answer each one out loud, and then write your answer in your own notes. The answers are yours to write, so this file leaves them blank.

Each module's questions are the ones its lesson lists under "Check your understanding". Modules whose lesson ends with an exit checklist have questions written from that checklist. Use the link to find the section that teaches the answer, and do not copy the answer from there.

## Python

### 01 Environment and tooling

[Lesson](../python/01-environment-tooling/lesson.md)

1. What is the difference between running a script and using the REPL?

   *Your answer:*

2. Why use a venv instead of installing globally?

   *Your answer:*

3. How do you know the venv is active?

   *Your answer:*

4. Why not commit `.venv`? What do you commit instead?

   *Your answer:*

5. In a traceback, which line do you read first?

   *Your answer:*

### 02 Syntax and data types

[Lesson](../python/02-core-syntax-data-types/lesson.md)

1. Why does `x = 20` not change `y` after `y = x`?

   *Your answer:*

2. Why is `0.1 + 0.2 == 0.3` False, and what do you use instead?

   *Your answer:*

3. What does `"hello"[1:4]` return, and `"hello"[::-1]`?

   *Your answer:*

4. Name 6 falsy values.

   *Your answer:*

5. What is the difference between `==` and `is`?

   *Your answer:*

6. What does `"" or "x"` return, and why?

   *Your answer:*

7. Why can't you change a character inside a string?

   *Your answer:*

### 03 Collections

[Lesson](../python/03-collections/lesson.md)

1. Why does `b = a; b.append(3)` change `a`? How do you avoid that?

   *Your answer:*

2. `sort()` vs `sorted()`: what does each return?

   *Your answer:*

3. Which collection would you use to check "has this user been seen before?" in a loop of a million items, and why?

   *Your answer:*

4. What happens on `d["missing"]` and how is `d.get("missing")` different?

   *Your answer:*

5. Why can a tuple be a dict key but a list can't?

   *Your answer:*

6. What is the result of `{1, 2, 3} & {2, 3, 4}`?

   *Your answer:*

### 04 Control flow

[Lesson](../python/04-control-flow/lesson.md)

1. What is the difference between `break` and `continue`?

   *Your answer:*

2. When does the `else` of a `for` loop run?

   *Your answer:*

3. Why prefer `enumerate` over `range(len(x))`?

   *Your answer:*

4. Rewrite `result = []; for n in nums: if n > 0: result.append(n*2)` as a comprehension.

   *Your answer:*

5. How do you stop an infinite `while True` loop from the code, and from the terminal?

   *Your answer:*

### 05 Functions

[Lesson](../python/05-functions/lesson.md)

1. Why is `def f(x, items=[])` a bug waiting to happen? What is the fix?

   *Your answer:*

2. What do `*args` and `**kwargs` hold inside the function?

   *Your answer:*

3. What does `LEGB` stand for, and what happens when you assign to a name inside a function?

   *Your answer:*

4. When do you need `nonlocal`?

   *Your answer:*

5. What is a closure? Give an example from memory.

   *Your answer:*

6. What is the base case of a recursive function and why does it matter?

   *Your answer:*

7. What makes a function "pure"?

   *Your answer:*

### 06 Modules, packages and the standard library

[Lesson](../python/06-modules-packages-stdlib/lesson.md)

1. What happens when you `import` a module twice?

   *Your answer:*

2. What does `if __name__ == "__main__":` do, and why use it?

   *Your answer:*

3. What makes a folder a package, and how do relative imports differ from absolute ones?

   *Your answer:*

4. Which tool counts words, which groups values into lists, and which caches a function's results?

   *Your answer:*

5. How do you add 7 days to a date and get the weekday name?

   *Your answer:*

6. Why use `pathlib` instead of joining strings with `/`?

   *Your answer:*

7. Why pass `ensure_ascii=False` when dumping Arabic text to JSON?

   *Your answer:*

### 07 Object-oriented programming

[Lesson](../python/07-oop/lesson.md)

1. What is the difference between an instance attribute and a class attribute? What happens if you assign `self.count = 5` when `count` is a class attribute?

   *Your answer:*

2. Why should every class have a `__repr__`?

   *Your answer:*

3. If you define `__eq__`, what happens to `__hash__`, and why does it matter?

   *Your answer:*

4. When would you use a property instead of a plain attribute?

   *Your answer:*

5. What does `super()` do, and how is it related to the MRO?

   *Your answer:*

6. When do you choose composition instead of inheritance?

   *Your answer:*

7. What does `@dataclass` generate? Why do you need `default_factory` for a list default?

   *Your answer:*

### 08 Error handling

[Lesson](../python/08-error-handling/lesson.md)

1. What is the difference between `else` and `finally` in a `try`?

   *Your answer:*

2. Why is a bare `except:` a bad idea?

   *Your answer:*

3. When do you write `raise ... from e`?

   *Your answer:*

4. What are `__enter__` and `__exit__` for, and what does returning `True` from `__exit__` do?

   *Your answer:*

5. Name one case where EAFP is better than an `if` check.

   *Your answer:*

6. Why make a base exception class for your own package?

   *Your answer:*

### 09 Iterators and generators

[Lesson](../python/09-iterators-generators/lesson.md)

1. What is the difference between an iterable and an iterator?

   *Your answer:*

2. What does a `for` loop do under the hood?

   *Your answer:*

3. What happens when you call a generator function? When does its body run?

   *Your answer:*

4. Why can a generator handle a 10 GB file but a list cannot?

   *Your answer:*

5. What does `yield from` do?

   *Your answer:*

6. Why does looping twice over the same generator give an empty second pass?

   *Your answer:*

### 10 Decorators

[Lesson](../python/10-decorators/lesson.md)

1. What does `@shout` above `def greet` expand to?

   *Your answer:*

2. Why do wrappers take `*args, **kwargs`?

   *Your answer:*

3. What does `functools.wraps` fix, and why does it matter?

   *Your answer:*

4. Why does `@repeat(3)` need three nested functions?

   *Your answer:*

5. In `@bold` over `@italic`, which runs first?

   *Your answer:*

6. Name three decorators you have used without writing them.

   *Your answer:*

### 11 Typing

[Lesson](../python/11-typing/lesson.md)

1. Does Python enforce type hints at runtime? Who does?

   *Your answer:*

2. What is the difference between `list[int]`, `Sequence[int]` and `Iterable[int]` as a parameter type?

   *Your answer:*

3. What does the checker force you to do with a value of type `int | None`?

   *Your answer:*

4. What does a `Protocol` give you that a base class does not?

   *Your answer:*

5. How do you write a function that returns the same type it received?

   *Your answer:*

6. How does a framework like FastAPI use your annotations?

   *Your answer:*

### 12 Concurrency and async

[Lesson](../python/12-concurrency-async/lesson.md)

1. When does `await asyncio.sleep(1)` let other tasks run, and why does `time.sleep(1)` inside an `async def` freeze all of them?

   *Your answer:*

2. For 200 HTTP calls, and for resizing images on an 8-core machine, which tool would you choose, and why: threads, processes or asyncio?

   *Your answer:*

3. What does calling `task.cancel()` do, and why must a `CancelledError` be raised again after you clean up?

   *Your answer:*

4. What does the GIL stop, and what does it leave alone?

   *Your answer:*

### 13 Testing

[Lesson](../python/13-testing/lesson.md)

1. How does pytest find tests, and why does a failing `assert` show so much detail?

   *Your answer:*

2. Why check the error message with `match` and not only the exception type?

   *Your answer:*

3. When do you use `parametrize`, and when a fixture?

   *Your answer:*

4. What does `tmp_path` give you, and why is it better than a real file?

   *Your answer:*

5. Dependency injection, `monkeypatch` and `Mock`: when do you pick each?

   *Your answer:*

6. Why is 100% coverage not proof of good tests? What does mutation testing add?

   *Your answer:*

### 14 Packaging

[Lesson](../python/14-packaging/lesson.md)

1. What is the difference between a module, a package and a distribution?

   *Your answer:*

2. What goes in `[build-system]` and what goes in `[project]`?

   *Your answer:*

3. Why use the `src` layout?

   *Your answer:*

4. What does `pip install -e .` do differently from `pip install .`?

   *Your answer:*

5. How does `[project.scripts]` turn a Python function into a shell command?

   *Your answer:*

6. When do you pin a dependency, and when do you give a range?

   *Your answer:*

7. Why do you never commit `.venv`, `dist/` or an upload token?

   *Your answer:*

### 15 Capstone: Task Tracker CLI

[Lesson](../python/15-capstone-task-tracker/README.md)

1. Why does only `storage.py` touch the file, and what does that make easier to test?

   *Your answer:*

2. Why do the capstone's rules turn exceptions into exit codes in one place, in `cli.py`?

   *Your answer:*

3. What does a dataclass's `__post_init__` guarantee about a `Task`, and what does it not guarantee?

   *Your answer:*

## Django

### 01 Architecture

[Lesson](../django/01-architecture/lesson.md)

1. Walk through what happens between typing `/hello/Sara/` and seeing the page, naming each layer.

   *Your answer:*

2. What is the difference between a project and an app?

   *Your answer:*

3. What do the `SECRET_KEY`, `DEBUG` and `INSTALLED_APPS` settings do, and which two are dangerous to get wrong in production?

   *Your answer:*

4. Why give URL patterns names? How do you use them in Python and in a template?

   *Your answer:*

5. What does `<int:a>` do, and what happens to `/add/x/2/`?

   *Your answer:*

6. What does template auto-escaping protect against?

   *Your answer:*

### 02 Models and the ORM

[Lesson](../django/02-models-orm/lesson.md)

1. What is a QuerySet, and why is it lazy?

   *Your answer:*

2. What do `on_delete=CASCADE` and `SET_NULL` do? When would you choose `PROTECT`?

   *Your answer:*

3. Why put a rule in a `CheckConstraint` and not only in Python?

   *Your answer:*

4. Why should you commit migrations, and never edit an applied one?

   *Your answer:*

5. What is the difference between `aggregate` and `annotate`? Show `GROUP BY` with `values().annotate()`.

   *Your answer:*

6. What is the N+1 problem, and how do `select_related` and `prefetch_related` fix it?

   *Your answer:*

7. Why store `weeks` and `per_week`, but compute `turns` and `payout`?

   *Your answer:*

### 03 Admin and forms

[Lesson](../django/03-admin-forms/lesson.md)

1. What is the difference between `list_display` and `search_fields`?

   *Your answer:*

2. What does an inline let a parent page do that a separate list page does not?

   *Your answer:*

3. In what order do the field checks, `clean_<field>()`, the form's `clean()` and the model's `clean()` run?

   *Your answer:*

4. Why must a model's `clean()` check for `None` before it compares dates, even though the form already checks the fields?

   *Your answer:*

5. A second `Book` with the same author and title is created from the shell with `Book.objects.create(...)`. Does the model's `clean()` stop it? What does, and what error do you get?

   *Your answer:*

6. When would you choose `forms.Form` over `ModelForm`?

   *Your answer:*

### 04 Views

[Lesson](../django/04-views/lesson.md)

1. When would you write a function view rather than a class-based view?

   *Your answer:*

2. What does Django return for a POST to a `View` that has only `get()`? Why?

   *Your answer:*

3. Why does `JsonResponse` need `safe=False` for a list?

   *Your answer:*

4. What does `DetailView` do before your `render_to_response()` runs?

   *Your answer:*

5. A reader posts a review for a book that is not published yet, with valid stars. The form passes. Why must the view check the book's publication date?

   *Your answer:*

6. Why does `get_object_or_404` matter more than `get()` for a URL like `/books/<int:pk>/`?

   *Your answer:*

### 05 Templates

[Lesson](../django/05-templates/lesson.md)

1. What does `render()` return, and what does it need?

   *Your answer:*

2. Why do templates live in `library/templates/library/`, not just in `templates/`?

   *Your answer:*

3. In a template, why does `{{ book.price_in_cents }}` work with no parentheses, and what happens if the method needs an argument?

   *Your answer:*

4. A member's name is `<script>alert(1)</script>`, and the template prints `{{ name }}`. Why does it show as text? Name two places where that protection is switched off.

   *Your answer:*

5. A base template has text inside `{% block content %}`. A child template extends it but does not define a `content` block. What appears on the page?

   *Your answer:*

6. What does `ListView` put in the context by default, and how do you change its name?

   *Your answer:*

7. A view puts `books` in the context, but the template loops over `{% for b in book_list %}`. What does the user see, and why is there no error?

   *Your answer:*

### 06 Django REST framework

[Lesson](../django/06-drf/lesson.md)

1. What does a `ModelSerializer` produce on output, and what does `is_valid()` check on input?

   *Your answer:*

2. Why is a `read_only` field ignored on input, and what does `source="published_on.year"` read?

   *Your answer:*

3. A client sends a second review for the same `(book, reader)` pair. Which layer returns the 400, and why must both fields be writable in the serializer?

   *Your answer:*

4. What does `ReadOnlyModelViewSet` give you, and what does the router add on top of it?

   *Your answer:*

5. An anonymous client sends a POST to a viewset with `TokenAuthentication`. Which status code does it get, and why would session authentication give a different one?

   *Your answer:*

6. Why does `?min_stars=abc` need a check inside `get_queryset()`, and why is `isdigit()` not enough?

   *Your answer:*

7. A list endpoint runs 1 query for the list and 1 query per row for a related field. What single change in `get_queryset()` fixes it?

   *Your answer:*

### 07 Middleware and signals

[Lesson](../django/07-middleware-signals/lesson.md)

1. In what order do `MIDDLEWARE` entries see a request, and in what order do they see the response?

   *Your answer:*

2. A middleware tries to set a response header before it calls `get_response`. What goes wrong, and why?

   *Your answer:*

3. Why must `AuthenticationMiddleware` come before a middleware that reads `request.user`?

   *Your answer:*

4. Why does `post_save` receive `created`, and why can a `pre_save` receiver not tell whether a row is new?

   *Your answer:*

5. A receiver is written and tested by hand, but the log never changes when a row is saved. What is the most likely cause?

   *Your answer:*

6. A rule says a reader cannot review the same book twice. Why is a `post_save` receiver the wrong place for it?

   *Your answer:*

7. A `bulk_create()` of 500 reviews runs. Which receivers run for those rows?

   *Your answer:*

### 08 Testing

[Lesson](../django/08-testing/lesson.md)

1. What does pytest-django do with each test's database changes, and why does that let tests run in any order?

   *Your answer:*

2. What goes wrong if `pytest.ini` has no `DJANGO_SETTINGS_MODULE` line?

   *Your answer:*

3. What does `ids=` add to a parametrized test?

   *Your answer:*

4. A fixture writes a row, and the test fails with a database-access error. What is missing?

   *Your answer:*

5. Why does `ReviewFactory(book__title="Dune")` change the title of a book it builds, and not of a review?

   *Your answer:*

6. Why must the `django_assert_num_queries` block contain only the request?

   *Your answer:*

7. A test calls `load_books()` and asserts nothing. Coverage shows 100 percent for that line. Why does that not prove the test is good?

   *Your answer:*

### 09 Caching and performance

[Lesson](../django/09-caching-performance/lesson.md)

1. Why does `select_related` use a join, while `prefetch_related` runs a second query?

   *Your answer:*

2. A loop uses `book.review_set.filter(stars=5)` after a prefetch. How many queries run, and why?

   *Your answer:*

3. What does `only("title")` cost if the loop later reads `book.summary`?

   *Your answer:*

4. Why does a `QuerySet.update()` leave a cached value stale, when a `save()` would not?

   *Your answer:*

5. Why must a test empty the cache before it starts?

   *Your answer:*

6. Why is it safer to clear a cache entry on commit than at the moment of the write?

   *Your answer:*

7. The cache loses all its entries. What still works, and what gets slower?

   *Your answer:*

### 10 Background tasks with Celery

[Lesson](../django/10-background-tasks/lesson.md)

1. Name the broker, the worker and beat, and say what each one does.

   *Your answer:*

2. Why does a Celery task take an ID rather than a model object?

   *Your answer:*

3. Name one error that a task should retry and one that it should not, and say why.

   *Your answer:*

4. How can a test in eager mode pass while the same task fails in production?

   *Your answer:*

### 11 Auth and security

[Lesson](../django/11-auth-security/lesson.md)

1. How do a session, a token and a JWT differ, and which one does a browser form use?

   *Your answer:*

2. What are the two DRF permission checks, and which one sees the object?

   *Your answer:*

3. Why does a token API need no CSRF token, while a form does?

   *Your answer:*

4. Name three cases where template escaping does not protect a page.

   *Your answer:*

### 12 Deployment

[Lesson](../django/12-deployment/lesson.md)

1. What are the six parts of a deployed app, and which setting controls each one?

   *Your answer:*

2. Why is `runserver` not used in production, and why does WhiteNoise matter?

   *Your answer:*

3. What does `DATABASE_URL` contain, and why keep SQLite for local work?

   *Your answer:*

4. Why must the server bind to `0.0.0.0:$PORT` in production?

   *Your answer:*

### 13 Capstone write-up

[Lesson](../django/13-capstone/lesson.md)

1. Why must every number in a write-up be measured, and how do you note the method?

   *Your answer:*

2. Why should the portfolio entry, the CV and the profile use the same numbers?

   *Your answer:*

3. What belongs in a case study's security section, and what should stay out of it?

   *Your answer:*

## FastAPI

### 10 FastAPI basics

[Lesson](../fastapi/10-basics/lesson.md)

1. In a route, which values come from the path, which from the query string, and which from the body?

   *Your answer:*

2. Which status codes fit a create, a delete, a not-found and a bad request?

   *Your answer:*

3. Why does a route need a response model when the stored row has a secret field?

   *Your answer:*

4. What goes wrong when you call `time.sleep` inside an `async def` route?

   *Your answer:*

### 10 Pydantic

[Lesson](../fastapi/10-pydantic/lesson.md)

1. How do you add a `Field` constraint, and where does it show up?

   *Your answer:*

2. Why must a Pydantic validator return the value it checks?

   *Your answer:*

3. Why does the input model refuse unknown fields, and what example shows the risk?

   *Your answer:*

4. How is a setting read from an environment variable, and why are settings not cached in the tests?

   *Your answer:*

### 11 Database

[Lesson](../fastapi/11-database/lesson.md)

1. Explain the engine, the session and `get_session`, and why `expire_on_commit` is off.

   *Your answer:*

2. How does a model's Python default differ from its database default, and which one does an old row get?

   *Your answer:*

3. How do you generate a migration, read it, apply it and undo it?

   *Your answer:*

4. Why does a new column that existing rows need a server default?

   *Your answer:*

### 11 Auth

[Lesson](../fastapi/11-auth/lesson.md)

1. What does `Depends` do, and why does a dependency that raises an exception stop the route?

   *Your answer:*

2. Why do passwords use a slow hash, and why does the hashing run in a thread?

   *Your answer:*

3. What does a JWT's payload reveal, and what does its signature prove?

   *Your answer:*

4. When does a protected route answer 401, and when does it answer 403?

   *Your answer:*

5. Why must a bad token never turn a request into an anonymous one?

   *Your answer:*

6. How do you override a dependency in a test, and why must the override be cleared afterwards?

   *Your answer:*

### 12 Background work and testing

[Lesson](../fastapi/12-background/lesson.md)

1. When does `BackgroundTasks` run, and what can it not do?

   *Your answer:*

2. What does a 202 response promise, and what does it not promise?

   *Your answer:*

3. Why does a background job open its own session, and why does it take ids rather than objects?

   *Your answer:*

4. How does `ondelete="CASCADE"` behave in SQLite, and why does the foreign-key PRAGMA matter?

   *Your answer:*

5. What does the test client do before it returns, and why does that matter for background work?

   *Your answer:*

6. How do you write an async test with the `anyio` marker?

   *Your answer:*

### 12 Docker and deployment

[Lesson](../fastapi/12-docker/lesson.md)

1. What goes into an image, and what does the container get from the environment at run time?

   *Your answer:*

2. Why does the order of Dockerfile instructions matter, and what is `.dockerignore` for?

   *Your answer:*

3. Why should the app run as a non-root user, listen on `0.0.0.0`, and start with `exec`?

   *Your answer:*

4. What do `docker inspect` and `docker history` reveal about a secret that went into the image?

   *Your answer:*

5. How does a named volume keep data when a container is replaced?

   *Your answer:*

6. What does a health check test, and which route and port does it use?

   *Your answer:*

### 12 Comparison with Django

[Lesson](../fastapi/12-comparison/comparison.md)

1. Where is Django the better choice, and where is FastAPI?

   *Your answer:*

2. What does Django's N+1 problem cost, and what does async SQLAlchemy do instead?

   *Your answer:*

### 13 Bonus: a real model and rate limits

[Lesson](../fastapi/13-ai-and-limits/lesson.md)

1. Why is the API key a `SecretStr`, and where may it appear and where not?

   *Your answer:*

2. Name the ways a call to a model's API can fail. Why do they all become one exception and a 502, and not a 500?

   *Your answer:*

3. Why does the summarizer run with `run_in_threadpool`, and how would a test show that it does?

   *Your answer:*

4. A prompt asks for at most 50 words and a JSON answer. Why does the code still check both?

   *Your answer:*

5. How does a sliding-window rate limit work, and what should `Retry-After` say?

   *Your answer:*

6. Why does a rate limit kept in memory break with several processes, or behind a proxy?

   *Your answer:*

7. How do you test an HTTP client without the network, and a limiter without waiting?

   *Your answer:*
