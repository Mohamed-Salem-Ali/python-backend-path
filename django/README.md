# Django (weeks 5–9)

Starts after the Python phase. The project is **Gameya**, a rotating-savings tracker, built step by step: models and ORM, admin, views and templates, tests, DRF, Celery, deployment.

Start with [WEEK-5.md](WEEK-5.md). The code lives in [`gameya_site/`](gameya_site/).

## Modules

| # | Folder | Topic | Week | Status | Files |
|---|---|---|---|---|---|
| 01 | [01-architecture](01-architecture/) | MTV, project vs app, request cycle | 5 | Ready | [lesson](01-architecture/lesson.md), [checks](gameya_site/circles/tests/test_architecture.py) |
| 02 | [02-models-orm](02-models-orm/) | Models, migrations, QuerySets | 5 | Ready | [lesson](02-models-orm/lesson.md), [model checks](gameya_site/circles/tests/test_models.py), [query checks](gameya_site/circles/tests/test_queries.py) |
| 03 | [03-admin-forms](03-admin-forms/) | Admin and forms | 6 | Ready | [lesson](03-admin-forms/lesson.md), [checks](gameya_site/circles/tests/test_admin_forms.py) |
| 04 | [04-views](04-views/) | Function and class-based views | 6 | Ready | [lesson](04-views/lesson.md), [checks](gameya_site/circles/tests/test_class_views.py) |
| 05 | [05-templates](05-templates/) | Templates, inheritance and static files | 6 | Ready | [lesson](05-templates/lesson.md), [checks](gameya_site/circles/tests/test_templates.py) |
| 06 | [06-drf](06-drf/) | Django REST Framework | 8 | Ready | [lesson](06-drf/lesson.md), [checks](gameya_site/circles/tests/test_api.py) |
| 07 | [07-middleware-signals](07-middleware-signals/) | Middleware and signals | 7 | Ready | [lesson](07-middleware-signals/lesson.md), [checks](gameya_site/circles/tests/test_middleware_signals.py) |
| 08 | [08-testing](08-testing/) | Testing with pytest-django and factories | 7 | Ready | [lesson](08-testing/lesson.md), [checks](gameya_site/circles/tests/test_pytest_suite.py) |
| 09 | [09-caching-performance](09-caching-performance/) | Caching and N+1 queries | 7 | Ready | [lesson](09-caching-performance/lesson.md), [checks](gameya_site/circles/tests/test_performance.py) |
| 10 | [10-background-tasks](10-background-tasks/) | Celery in eager mode | 9 | Ready | [lesson](10-background-tasks/lesson.md), [checks](gameya_site/circles/tests/test_tasks.py) |
| 11 | [11-auth-security](11-auth-security/) | Auth and security | 9 | Ready | [lesson](11-auth-security/lesson.md), [checks](gameya_site/circles/tests/test_security.py), [security review](11-auth-security/security-review.md) |
| 12 | [12-deployment](12-deployment/) | Deployment | 9 | Ready | [lesson](12-deployment/lesson.md), [checks](gameya_site/circles/tests/test_deployment.py), [deploy checklist](12-deployment/deploy-checklist.md) |
| 13 | [13-capstone](13-capstone/) | Gameya portfolio project (write-up) | 9 | Ready | [lesson](13-capstone/lesson.md), [case study template](13-capstone/case-study-template.md) |

Module folders are created as each lesson is written. Until then, the syllabus is the source for each topic.

## Files in this folder

| File | What it is |
|---|---|
| [SYLLABUS.md](SYLLABUS.md) | Core track, project, exit exam, advanced tier |
| [WEEK-5.md](WEEK-5.md) | Week 5 goals and daily plan |
| [gameya_site/](gameya_site/) | The Django project (see its [README](gameya_site/README.md)) |

## Run the project

```bash
cd django/gameya_site
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python manage.py test
```

Django must be installed first. The [week 5 setup](WEEK-5.md#setup-day-1-15-minutes) walks you through it.

The tests in `gameya_site/circles/tests/` are the specification. Most fail until you build the feature they describe.

See the [syllabus](SYLLABUS.md) and [the 12-week plan](../docs/12-week-plan.md) for the full outline.
