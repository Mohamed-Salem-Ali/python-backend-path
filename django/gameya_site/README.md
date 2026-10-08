# gameya_site

The Django project for **Gameya**, the rotating-savings tracker. You build it one module at a time. The app files start as stubs with `TODO`s, and the tests describe what each one must do.

## Layout

| Path | What it is | State |
|---|---|---|
| [manage.py](manage.py) | Django's command-line entry point | Ready |
| [requirements.txt](requirements.txt) | Packages needed to run the project | Ready |
| [config/](config/) | Settings, root URL routes, WSGI and ASGI entry points | Ready |
| [circles/](circles/) | The app that holds the Gameya domain | Scaffold |
| [circles/models.py](circles/models.py) | Four models: `Gameya`, `Member`, `Payment`, `PayoutSlot` | Stub (module 02) |
| [circles/queries.py](circles/queries.py) | Reusable query functions | Stub (module 02) |
| [circles/views.py](circles/views.py) | Health, hello, add and about views | TODO comments only (module 01) |
| [circles/urls.py](circles/urls.py) | App URL routes | TODO comments only (module 01) |
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

Run them from this folder, after the [week 5 setup](../WEEK-5.md#setup-day-1-15-minutes):

```bash
python manage.py test
```

Do not edit the test files. Most tests fail until you build the feature they describe. A few wiring checks pass from the start. That is intended.
