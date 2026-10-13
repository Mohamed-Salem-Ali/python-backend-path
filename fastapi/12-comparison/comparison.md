# Django or FastAPI? What the two tracks teach you

This course builds two projects with two frameworks. Gameya, in the Django track, is a savings-circle app with users, pages, an admin, a JSON API and a weekly background report. The Study API, in the FastAPI track, is an API that stores summaries, signs users in, and makes flashcards in the background. The projects differ in scope, so a difference in code size or test count mostly reflects scope, not the framework. This note compares the tools, and it points to the lessons where each behavior is shown.

## The short answer

- **Choose Django** when the product is a web application: users who sign in, pages and forms, an admin that staff use every day, and a data model that changes often. Most of that comes from the framework, so you spend your time on the product.
- **Choose FastAPI** when the product is an API, or a service behind one, that other programs call. It fits work that waits on other services, such as a model provider, and it fits a team that wants request and response shapes checked and documented from the type hints. You assemble more yourself.
- **Django with Django REST framework** is also a sound API choice. The gap between the two is smaller than the slogans suggest. It lies in defaults, in how each handles async work, and in how much you assemble yourself.

## Side by side

| Topic | Django (with DRF) | FastAPI |
|---|---|---|
| Shape | Batteries included: ORM, admin, forms, templates, auth and migrations in one project | A small core: routing, validation and docs. You choose the database library, the migration tool and the auth parts |
| Models and migrations | Django ORM. Migrations are generated per app and tracked for you | SQLAlchemy 2.0 models. Alembic generates migrations, and you read each one before you apply it |
| Validation | DRF serializers for the API, forms for HTML | Pydantic models for bodies, responses and settings |
| API docs | DRF's browsable API, and schema tools as add-ons | OpenAPI generated from the type hints. `/docs` is on by default |
| Auth | An auth app with users, sessions and permissions. JWT comes from a library (simplejwt) | You assemble it: hashing, tokens, and the dependency that reads them |
| Admin | Built in for every model you register | None. You build the screens, or use a separate tool |
| Background work | Celery is the usual choice, with retries and a scheduler (beat) | `BackgroundTasks` runs in the web process. A queue such as Celery is needed for work that must survive a restart |
| Async | Views can be async, and the ORM has async methods. The Gameya project uses the synchronous ORM | Async from the start: routes, database sessions, and outside calls. Sync routes run in a thread pool |
| Tests | pytest-django, factory-boy and the test client. Each test gets a clean database | `TestClient`, dependency overrides, and `anyio` for async tests |
| Production checks | `manage.py check --deploy` lists unsafe settings | No built-in equivalent. The Study API tests its Dockerfile and its settings directly |

## Three places the difference showed up

**1. Loading related rows.** In Django, a loop that reads a related object for each row runs one query per row, and nothing warns you. The fix is `select_related` or `prefetch_related` ([Django lesson 02](../../django/02-models-orm/lesson.md), section 9, and [module 09](../../django/09-caching-performance/lesson.md)). In async SQLAlchemy, the same lazy load raises `MissingGreenlet` instead, because the session cannot load data implicitly inside async code ([FastAPI database lesson](../11-database/lesson.md)). Django is quiet and slow, and SQLAlchemy is loud and fails fast. Both need you to load what you use.

**2. Object permissions.** In DRF, `has_permission` runs on every request, and `has_object_permission` runs only when a view loads one object. `BasePermission.has_object_permission` returns `True` by default, so a permission class with only `has_permission` lets any signed-in user change any row. This is the most common ownership bug in DRF ([Django lesson 11](../../django/11-auth-security/lesson.md)). In the Study API, the owner check is a line in the route, which is easy to see and also easy to forget. The delete route there is still open to any caller, and [the auth lesson](../11-auth/lesson.md) names it as a gap. Both frameworks leave the ownership check to you.

**3. Background work.** Celery runs tasks in a separate worker, with retries, schedules and an eager mode for tests ([Django lesson 10](../../django/10-background-tasks/lesson.md)). `BackgroundTasks` runs a function after the response, in the same process. The test client waits for it, so route tests stay simple. It has no retries, and a restart loses the work. The question to ask is how much you can afford to lose, more than which framework you use. The [FastAPI background lesson](../12-background/lesson.md) covers when to move to a queue.

## Where each is the better choice

**Django** is the better choice when:

- Most of the work is screens, forms, content and per-user permissions.
- Staff need an admin on day one, and the data changes often enough that the admin pays for itself.
- A team wants conventions that every member already knows, so the code reads the same everywhere.
- The work is mostly database reads and writes, with few outside calls that take seconds.

**FastAPI** is the better choice when:

- Other programs call the API, or a separate frontend does, so the response shape is the product.
- Requests spend most of their time waiting on outside services, such as a model provider, and you want that wait to be async.
- You want validation and documentation generated from the same type hints, so they cannot drift apart.
- The service is small, and you are happy to choose and wire the parts yourself.

**Either** needs the same things beyond the framework: a real database in production, a container, tests that run in CI, and a plan for work that must not be lost.

## What this comparison does not show

- **Speed.** We did not benchmark the two. A fair comparison needs the same workload and the same server setup, such as gunicorn with workers for Django and uvicorn for FastAPI, and it would mostly measure the database. Do not choose a framework on a benchmark run in a development server.
- **Hiring and ecosystem size.** Both have large communities, and this note does not compare them.

## How to check the facts here

The test counts are functions in the repo's test files. They are not a measure of quality, and the projects differ in scope. Run these from the repo root:

```bash
grep -rhE "^\s*def test_" django/gameya_site/circles/tests/ | wc -l
grep -rhE "^(async )?def test_" fastapi/study-api/tests/ | wc -l
```

The first prints 254, and the second prints 88 at the time of writing. The Django count includes the methods inside `TestCase` classes, which is why its pattern allows leading spaces; the Study API's tests are all plain functions. A few Django tests are parametrized, so pytest runs slightly more Django cases than the count shows. Each lesson named above has a section that shows the behavior with a short example. The [Study API](../study-api/) holds the FastAPI side, and the [Gameya project](../../django/gameya_site/) holds the Django side.
