# gameya_site

The Django project for **Gameya**, the rotating-savings tracker. You build it one module at a time. The app files start as stubs with `TODO`s, and the tests describe what each one must do.

## Layout

| Path | What it is | State |
|---|---|---|
| [manage.py](manage.py) | Django's command-line entry point | Ready |
| [requirements.txt](requirements.txt) | Packages needed to run the project | Ready |
| [config/](config/) | Settings, root URL routes, WSGI and ASGI entry points | Ready |
| [config/celery.py](config/celery.py) | The Celery app that runs background tasks | Stub (module 10) |
| [circles/](circles/) | The app that holds the Gameya domain | Scaffold |
| [circles/models.py](circles/models.py) | Four models: `Gameya`, `Member`, `Payment`, `PayoutSlot`. Module 07 adds `AuditEntry` | Stub (module 02) |
| [circles/queries.py](circles/queries.py) | Reusable query functions | Stub (module 02) |
| [circles/views.py](circles/views.py) | Function views (health, hello, add, about) and class-based views (list, detail, payments) | TODO comments only (modules 01, 04 and 05) |
| [circles/urls.py](circles/urls.py) | App URL routes | TODO comments only (modules 01, 04, 05 and 06) |
| [circles/serializers.py](circles/serializers.py) | Serializers: `GameyaSerializer` and `MemberSerializer` | TODO comments only (module 06) |
| [circles/api.py](circles/api.py) | The REST API: permission, pagination and viewsets | TODO comments only (module 06) |
| [circles/middleware.py](circles/middleware.py) | `RequestIdMiddleware`: a request id on every request and response | TODO comments only (module 07) |
| [circles/signals.py](circles/signals.py) | Receivers that write the audit log for payments and members, and clear the summary cache | TODO comments only (modules 07 and 09) |
| [circles/caching.py](circles/caching.py) | The gameya summary: built with few queries, kept in the cache, and cleared on change | TODO comments only (module 09) |
| [circles/tasks.py](circles/tasks.py) | Background tasks: the week rule, the unpaid-payments report, and the job the schedule runs | Stub (module 10) |
| [pytest.ini](pytest.ini) | pytest settings: which Django settings to use, and where the tests are | TODO comments only (module 08) |
| [circles/tests/factories.py](circles/tests/factories.py) | Factories that build test data: gameyas, members and payments | TODO comments only (module 08) |
| [circles/tests/conftest.py](circles/tests/conftest.py) | Shared pytest fixtures: a gameya, staff and reader users and tokens, and clients | TODO comments only (module 08) |
| `circles/templates/circles/` | HTML templates: base layout, home and gameya pages (module 05) | You create these |
| `circles/static/circles/` | CSS for the pages (module 05) | You create this |
| `circles/templates/circles/about.html` | About page template. You create this file | Module 01 |
| [circles/admin.py](circles/admin.py) | Admin registrations | TODO comments only (module 03) |
| [circles/forms.py](circles/forms.py) | `PaymentForm` and `JoinForm` | TODO comments only (module 03) |
| [circles/migrations/](circles/migrations/) | Generated migration files | Created by `makemigrations` |
| [circles/tests/](circles/tests/) | Acceptance tests (see below) | Ready |

## Tests

| File | Covers | Module |
|---|---|---|
| [test_architecture.py](circles/tests/test_architecture.py) | URLs, views and templates | 01 |
| [test_models.py](circles/tests/test_models.py) | The four models, their relations and constraints | 02 |
| [test_queries.py](circles/tests/test_queries.py) | The functions in `queries.py`, including query counts | 02 |
| [test_admin_forms.py](circles/tests/test_admin_forms.py) | The admin registrations, admin pages, and the forms | 03 |
| [test_class_views.py](circles/tests/test_class_views.py) | The class-based views: list, detail and payments API | 04 |
| [test_templates.py](circles/tests/test_templates.py) | The HTML pages, template inheritance, escaping and static files | 05 |
| [test_api.py](circles/tests/test_api.py) | The REST API: serializers, viewsets, routes, tokens, permissions, pagination and filters | 06 |
| [test_middleware_signals.py](circles/tests/test_middleware_signals.py) | The request id middleware and the audit log receivers | 07 |
| [test_pytest_suite.py](circles/tests/test_pytest_suite.py) | pytest tests: parametrized rules, factories, fixtures, the client and query counts. Run with `pytest` | 08 |
| [test_performance.py](circles/tests/test_performance.py) | pytest tests: query counts for the summary, the cache, and its invalidation. Run with `pytest` | 09 |
| [test_tasks.py](circles/tests/test_tasks.py) | pytest tests: the Celery app and schedule, the week rule, the report task and its retries. Run with `pytest` | 10 |

Run them from this folder, after the [week 5 setup](../WEEK-5.md#setup-day-1-15-minutes):

```bash
python manage.py test
```

Do not edit the `test_*.py` files. Most tests fail until you build the feature they describe. A few wiring checks pass from the start. That is intended. The module 08 stubs, `factories.py` and `conftest.py`, are yours to fill in.

`python manage.py test` also loads `test_pytest_suite.py`, which imports pytest. That is why `requirements.txt` includes pytest, pytest-django and factory-boy from the start. The module 08 tests are plain pytest functions, so run that file with pytest, not `manage.py test`:

```bash
pytest circles/tests/test_pytest_suite.py
```

Modules 09 and 10 are pytest files too: `pytest circles/tests/test_performance.py` and `pytest circles/tests/test_tasks.py`.
