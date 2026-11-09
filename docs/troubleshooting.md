# Troubleshooting

The errors learners hit most often, with the message you see, why it happens and the fix. Every message here was copied from a real run on this repo. Search this page for the last line of your error (Ctrl+F); that line names the problem.

If your error is not here, read [how to learn](how-to-learn.md) rule 2 first: read the traceback from the bottom, and give it ten minutes. Then open an issue with the command you ran and the whole message.

## Setup, all tracks

### PowerShell will not activate the virtual environment

```text
.venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system.
```

**Why:** Windows PowerShell blocks scripts by default, and `Activate.ps1` is a script.

**Fix:** allow scripts that you created yourself, for your user only, then activate again:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.venv\Scripts\Activate.ps1
```

If you would rather not change the policy, skip activation and call the environment's Python by its path: `.venv\Scripts\python -m pytest`.

### A package you installed is "not found"

```text
ModuleNotFoundError: No module named 'rest_framework'
```

**Why:** the command ran with a different Python from the one you installed into. Usually the virtual environment is not active, or it is the environment of the other project: the Django and FastAPI projects each have their own.

**Fix:** activate the environment of the folder you are in, then install that folder's requirements:

```bash
cd django/gameya_site            # or fastapi/study-api
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

`python -c "import sys; print(sys.executable)"` prints which Python is running. It should end in `.venv/bin/python` or `.venv\Scripts\python.exe`.

### A command cannot find its project

```text
can't open file '...\python-backend-path\django\manage.py': [Errno 2] No such file or directory
ModuleNotFoundError: No module named 'app'
FAILED: No 'script_location' key found in configuration.
```

**Why:** `manage.py`, `uvicorn app.main:app` and `alembic` look in the current folder. The three lines above are `manage.py` run from `django/`, and `uvicorn` and `alembic` run from the repo root.

**Fix:** `cd django/gameya_site` for Django, and `cd fastapi/study-api` for the Study API, before you run them.

### The port is already in use

```text
ERROR:    [Errno 10048] error while attempting to bind on address ('127.0.0.1', 8765): [winerror 10048] only one usage of each socket address (protocol/network address/port) is normally permitted
```

On macOS and Linux the same problem reads `[Errno 48] Address already in use` or `[Errno 98] Address already in use`.

**Why:** another server is still running on that port, often one you started earlier in another terminal.

**Fix:** stop the other server with Ctrl+C in its terminal, or start this one on another port: `uvicorn app.main:app --port 8001`, or `python manage.py runserver 8001`.

## Python track

### An exercise stops with a bare `AssertionError`

```text
  File "...\python\02-core-syntax-data-types\exercises.py", line 67, in <module>
    assert average3(1, 2, 6) == 3.0
           ^^^^^^^^^^^^^^^^^^^^^^^^
AssertionError
```

**Why:** that is the check working. The line above `AssertionError` is the first check your code does not pass yet. A fresh clone stops on the first check of every module, because every function is still a `TODO`.

**Fix:** call the function yourself and compare: `python -c "from exercises import average3; print(average3(1, 2, 6))"`, run from the module's folder. On a fresh clone it prints `None`, because the `TODO` body returns nothing yet. Then fix the function and run the file again. The checks run in order, so each fix moves the stop further down.

### Module 13 says "Not yet"

```text
Not yet: 11 place(s) in test_payments.py still say NotImplementedError.
```

**Why:** the checker grades the tests you write, and your test file still has the placeholders.

**Fix:** replace each `raise NotImplementedError` in `test_payments.py` with a real test, as the [lesson](../python/13-testing/lesson.md) explains. The checker then plants bugs in a copy of the code and reports which ones your tests miss.

## Django track

Run these from `django/gameya_site`.

### `pytest` stops before any test runs

```text
django.core.exceptions.ImproperlyConfigured: Requested setting AUTH_USER_MODEL, but settings are not configured. You must either define the environment variable DJANGO_SETTINGS_MODULE or call settings.configure() before accessing settings.
```

**Why:** pytest does not know which settings module to load until `pytest.ini` names it. That is TODO 28, in module 08.

**Fix:** before module 08, run the tests with Django's own runner: `python manage.py test circles.tests.test_models`. From module 08 on, finish TODO 28. To run pytest before that, name the settings on the command line: `pytest --ds=config.settings`.

### "Got unexpected keyword arguments"

```text
TypeError: Gameya() got unexpected keyword arguments: 'name', 'start_date', 'weeks', 'share_value'
```

**Why:** a test creates a model with fields that your model does not have yet. On a fresh clone, every model is still a `TODO`.

**Fix:** add the fields the error lists to the model, following [module 02](../django/02-models-orm/lesson.md), then make and apply the migration (next entry).

### "No such table" or "has no column"

```text
django.db.utils.OperationalError: no such table: auth_user
django.db.utils.OperationalError: no such table: circles_gameya
django.db.utils.OperationalError: table circles_gameya has no column named weeks
```

**Why:** the database is behind the models. Either `migrate` never ran (the first two), or you changed a model without making a migration for the change (the third). `migrate` warns about the second case, and the warning is easy to miss:

```text
Your models in app(s): 'circles' have changes that are not yet reflected in a migration, and so won't be applied.
```

**Fix:** make a migration for every model change, read it, then apply it:

```bash
python manage.py makemigrations circles
python manage.py migrate
```

The test runner builds its own database from the migrations, so a model change without a migration fails the tests in the same way.

## FastAPI track (the Study API)

Run these from `fastapi/study-api`.

### Every test fails with "TODO 7"

```text
E       NotImplementedError: TODO 7
```

**Why:** each test starts by loading the settings (TODO 7, the Pydantic lesson) and migrating a test database (the database lesson). Until both exist, no test can start, whatever you have written. In week 10 this is expected.

**Fix:** in week 10, check your routes in the browser instead: `uvicorn app.main:app --reload`, then `http://127.0.0.1:8000/docs`. The [Study API README](../fastapi/study-api/README.md#tests) lists when each test file starts to run.

### The app refuses to start: `secret_key`

```text
pydantic_core._pydantic_core.ValidationError: 1 validation error for Settings
secret_key
  Field required [type=missing, input_value={}, input_type=dict]
```

or, with a key that is too short:

```text
secret_key
  String should have at least 32 characters [type=string_too_short, input_value='short', input_type=str]
```

**Why:** from the auth lesson on, the app needs `STUDY_SECRET_KEY` to sign tokens, and it refuses to start without a long one, on purpose. `alembic` and `uvicorn` both load the settings, so both stop.

**Fix:** generate a key and set it in the same terminal:

```bash
python -c "import secrets; print(secrets.token_urlsafe(48))"
export STUDY_SECRET_KEY="paste-the-key-here"          # PowerShell: $env:STUDY_SECRET_KEY = "..."
```

The tests set their own key, so `pytest` does not need it.

### The server answers 500: "no such table"

```text
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: summaries
```

**Why:** the server's database file, `study.db`, has never been migrated. The tests migrate their own database, so they can pass while the server fails.

**Fix:** `alembic upgrade head`, with `STUDY_SECRET_KEY` set, then start the server again.

### "The migrations match the models" fails

```text
E       AssertionError: [('add_column', None, 'flashcards', Column('hint', String(), table=<flashcards>))]
```

**Why:** a model and the migrations disagree. Here a `hint` column was added to the `Flashcard` model with no migration for it. The test lists each difference: `add_column`, `remove_column`, `add_table` and so on.

**Fix:** generate a migration for the change, read it, and apply it:

```bash
alembic revision --autogenerate -m "add hint"
alembic upgrade head
```

If you edited a migration that already ran, do not edit it again: write a new one. The [database lesson](../fastapi/11-database/lesson.md), section 4, explains why.

## Still stuck?

- `python scripts/progress.py` shows which modules and test files pass, so you can see whether the problem is new.
- Re-read the end of the module's lesson. Every lesson closes with at least one of "Common mistakes", "Habits", "Check your understanding" or an exit checklist, and the mistake you made is often listed there.
- Open an issue with the command, the whole error, and what you already tried.
