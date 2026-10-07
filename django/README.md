# Django (weeks 5–9)

Starts after the Python phase. The project is **Gameya**, a rotating-savings tracker, built step by step: models and ORM, admin, views and templates, tests, DRF, Celery, deployment.

| Week | Start here | Status |
|---|---|---|
| 5 | [WEEK-5.md](WEEK-5.md): architecture, models and the ORM | Ready |
| 6 | Admin, forms, views and templates | Planned |
| 7 | Middleware, signals, testing, performance | Planned |
| 8 | Django REST Framework | Planned |
| 9 | Celery, auth and security, deployment | Planned |

The code lives in [`gameya_site/`](gameya_site/). Each module has a `lesson.md`; the tests in `gameya_site/circles/tests/` are the specification. They fail until you build the feature.

```bash
cd django/gameya_site
python -m venv .venv && .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py test
```

See the [syllabus](SYLLABUS.md) and [../docs/12-week-plan.md](../docs/12-week-plan.md) for the full outline.
