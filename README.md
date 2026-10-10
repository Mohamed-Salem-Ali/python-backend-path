# Python Backend Path

A hands-on, ground-up path through **Python → Django → FastAPI** in 12 weeks, at 2–5 hours a day. Each module has a lesson and a way to check your work, and the weeks build toward two deployed projects.

It is written in the open by a working developer relearning the fundamentals properly. Follow along, fork it, or open an issue if something is unclear.

## How it works
1. Read the **lesson** (`lesson.md`) and type every example yourself.
2. Fill in the `TODO`s in **`exercises.py`** and run it. A passing file prints `All checks passed`. Django and the capstone are checked by tests instead.
3. Finish the week's **project**.
4. Write down what you learned. Tick the checkpoint.

Exercises start as stubs on purpose, so a fresh clone fails until you do the work.

## Quick start
Requires Python 3.12+.

```bash
git clone https://github.com/Mohamed-Salem-Ali/python-backend-path.git
cd python-backend-path
python -m venv .venv

# Windows PowerShell
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install -r requirements-dev.txt
python python/01-environment-tooling/exercises.py
```

## Roadmap
The week-by-week plan is in [docs/12-week-plan.md](docs/12-week-plan.md). Day-by-day detail is in each `WEEK-N.md` file.

| Weeks | Phase | Status |
|---|---|---|
| 1–4 | [Python fundamentals](python/SYLLABUS.md) | 14 of 15 modules ready. Module 12 (concurrency) is planned for week 10 |
| 5–9 | [Django](django/SYLLABUS.md): models, views, admin, DRF, Celery, deployment | 12 of 13 modules ready (architecture, models, admin and forms, views, templates, DRF, middleware and signals, testing, caching and performance, background tasks, auth and security, deployment) |
| 10–12 | [FastAPI](fastapi/SYLLABUS.md): async, Pydantic, SQLAlchemy, JWT, Docker | Planned (9 topics over 3 weeks, none written yet) |

### Python modules
| # | Module | Week | Status |
|---|---|---|---|
| 01 | [Environment and tooling](python/01-environment-tooling/lesson.md) | 1 | Ready |
| 02 | [Syntax and data types](python/02-core-syntax-data-types/lesson.md) | 1 | Ready |
| 03 | [Collections](python/03-collections/lesson.md) | 1 | Ready |
| 04 | [Control flow](python/04-control-flow/lesson.md) | 1 | Ready |
| 05 | [Functions](python/05-functions/lesson.md) | 2 | Ready |
| 06 | [Modules, packages and the standard library](python/06-modules-packages-stdlib/lesson.md) | 2 | Ready |
| 07 | [OOP](python/07-oop/lesson.md) | 3 | Ready |
| 08 | [Error handling](python/08-error-handling/lesson.md) | 2 | Ready |
| 09 | [Iterators and generators](python/09-iterators-generators/lesson.md) | 3 | Ready |
| 10 | [Decorators](python/10-decorators/lesson.md) | 3 | Ready |
| 11 | [Typing](python/11-typing/lesson.md) | 4 | Ready |
| 12 | Concurrency and async | 10 | Planned |
| 13 | [Testing](python/13-testing/lesson.md) | 4 | Ready |
| 14 | [Packaging](python/14-packaging/lesson.md) | 4 | Ready |
| 15 | [Capstone: Task Tracker CLI](python/15-capstone-task-tracker/README.md) | 4 | Ready |

Module 13 is checked differently: you write `test_payments.py`, and `check_tests.py` grades it. The lesson explains how. Every other Python module uses `exercises.py`.

Per-folder summaries are in each track's README: [python/](python/README.md), [django/](django/README.md), [fastapi/](fastapi/README.md), [docs/](docs/README.md).

### Revision companions
Optional interactive summaries made with Google NotebookLM. Use them for a recap after you finish a lesson; the lessons stay the source of truth, and the links are hosted by Google.

| Module | Companion |
|---|---|
| 01 Environment and tooling | [Mastering Python Foundations](https://notebooklm.link.google/0LMX09CyQQoX) |
| 02 Syntax and data types | [Core Syntax and Data Types](https://notebooklm.link.google/WGAvifLEKiA1) |
| 03 Collections | [Mastering Python Collections](https://notebooklm.link.google/nfBMqTXIerPx) |
| 04 Control flow | [Python Control Flow](https://notebooklm.link.google/BypzOY5qK266) |

## Repository layout
```text
python/    SYLLABUS.md, lessons, exercises and projects (weeks 1-4, module 12 in week 10)
django/    SYLLABUS.md, the Django project (gameya_site/) and lessons (weeks 5-9)
fastapi/   SYLLABUS.md and README (weeks 10-12, not written yet)
docs/      the 12-week plan and the how-to-learn guide
```

Each track has its own syllabus with an exit exam (what "I know it" means) and an advanced tier for going deeper after week 12.

## Learning rules
See [docs/how-to-learn.md](docs/how-to-learn.md). In short: predict before you run, read errors from the bottom, and explain each idea out loud.

## Contributing
Found a typo, a wrong check, or a confusing explanation? Please open an issue or a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License
[MIT](LICENSE)
