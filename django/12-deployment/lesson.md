# Module 12 (Django): Deployment

By the end you can say what a deployed Django app is made of, serve its static files, run it with gunicorn, switch its database with an environment variable, start it on Render, and check it after each deploy.

**Before you start:** finish modules 02 to 11. Module 11's production settings are the base of this module.

**Setup:** this module adds three packages: gunicorn, whitenoise and psycopg. From `django/gameya_site`:

```bash
pip install -r requirements.txt
```

gunicorn does not run on Windows. You can still install it, and the tests check its configuration, not its process. To run gunicorn itself, use WSL, or let Render run it for you. The Render steps are in section 6.

Run this module's tests with `pytest circles/tests/test_deployment.py`. All 9 should pass when you finish.

**How to read the examples:** the examples use a made-up `notes` app. It is not part of gameya_site.

## 1. What a deployed app is made of
Running `runserver` on your laptop uses six parts that a server has to provide itself:

| Part | Locally | On a server |
|---|---|---|
| Code | your folder | a copy of the repo, built on the host |
| Settings | defaults, DEBUG on | environment variables, DEBUG off |
| Static files (CSS, admin JavaScript) | Django serves them | collected into one folder, served by WhiteNoise |
| Database | a SQLite file | PostgreSQL, a separate service that outlives the app |
| App server | `runserver` (not for production) | gunicorn, which runs several worker processes |
| Address and HTTPS | `127.0.0.1:8000` | a public host name with a certificate |

Each section below covers one row.

## 2. The three production packages
- **gunicorn** runs the app. It starts worker processes and hands requests to them. `runserver` is single-process and checks for code changes, so it is slow and unsafe for production.
- **whitenoise** serves static files from the app itself. Without it, the admin pages lose their CSS once DEBUG is off.
- **psycopg** is the PostgreSQL driver. Django needs a driver for every database engine it talks to.

All three are pinned in `requirements.txt` with a version range, like the other packages.

**Try it:** run `pip show gunicorn whitenoise psycopg` and read the version of each. Then open `requirements.txt` and check that each name has a range that includes the version you see.

## 3. Static files
In development, Django serves static files itself. In production it does not, so you need two things:

1. `STATIC_ROOT`: the folder where `collectstatic` copies every static file, from the admin and from your app.
2. WhiteNoise: a middleware that serves that folder. It must sit directly after `SecurityMiddleware`, so that it runs early.

```python
# Made-up example: the notes app
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # ...the rest, unchanged
]
```

The build runs `collectstatic` before the app starts, so the folder exists on the server. The folder is git-ignored, because it is built output. Until you run `collectstatic`, WhiteNoise prints a warning that the folder is missing whenever the app loads, including in the tests. The warning is harmless.

**Try it:** run `python manage.py collectstatic --noinput --dry-run`. Read the count it prints. Then run it without `--dry-run`, and open `staticfiles/admin/css/` to see the files it copied. Run `git status`: the folder should not appear, because it is git-ignored.

## 4. The database from the environment
Locally the project uses a SQLite file. A server's disk is not a safe place for data: hosts rebuild or replace the disk on a redeploy. Use PostgreSQL, a separate service, and give the app its address in one variable, `DATABASE_URL`:

```
postgres://<user>:<password>@<host>:<port>/<name>
```

The settings read that URL when it is set, and keep SQLite when it is not:

```python
# Made-up example: the notes app
import os
from urllib.parse import urlparse

DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}}

if os.environ.get("DATABASE_URL"):
    url = urlparse(os.environ["DATABASE_URL"])
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": url.path.lstrip("/"),
            "USER": url.username,
            "PASSWORD": url.password,
            "HOST": url.hostname,
            "PORT": str(url.port or 5432),
        }
    }
```

Migrations are a separate step. The app does not run them by itself, so the start command runs `migrate` (section 6).

**Try it:** set `DATABASE_URL` to a fake PostgreSQL address and print the engine and host from the Django shell. On Windows PowerShell, set the variable first with `$env:DATABASE_URL = "postgres://user:password@localhost:5432/notes"`, then run:

```bash
python manage.py shell -c "from django.conf import settings as s; print(s.DATABASES['default']['ENGINE'], s.DATABASES['default']['HOST'])"
```

Django does not connect when it only reads settings, so no database needs to exist for this check.

## 5. The app server
The command that starts the app is:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

Read the parts: `config.wsgi:application` names the WSGI entry point that `startproject` created. `--bind 0.0.0.0:$PORT` listens on every network interface, on the port that the host provides in the `PORT` variable. A server bound to `127.0.0.1` cannot be reached from outside the host, and that is the most common reason a deploy shows a timeout.

## 6. Render
Render runs the three parts of the build for you: it installs the requirements, runs the start command, and keeps the service running.

1. In the Render dashboard, choose New, then Web Service, and connect the `python-backend-path` GitHub repo.
2. Set **Root Directory** to `django/gameya_site`. The project lives in a subfolder, so Render must start there.
3. Set **Runtime** to Python. Set **Build Command** to `pip install -r requirements.txt && python manage.py collectstatic --noinput`.
4. Set **Start Command** to `python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`.
5. Under Environment, add: `PYTHON_VERSION` as `3.12.6`; `DJANGO_PRODUCTION` as `1`; `DJANGO_SECRET_KEY`, using Render's generate option; `DJANGO_ALLOWED_HOSTS` as the service's host name, which ends in `.onrender.com`; and `DATABASE_URL`, which you copy from a PostgreSQL database you create on Render in the same region.
6. Deploy. Read the build log, then the runtime log.

`render.yaml` in this folder records the same settings as a file. Render reads a blueprint only from the root of the repository, so the dashboard steps above are what actually runs. Keep the file in step with the dashboard, so the next person can read the settings in one place.

Two notes about Render's free plan. A free web service sleeps after 15 minutes without traffic, and the first request after that waits about a minute. A free PostgreSQL database expires after a fixed period, and the limit changes, so read the current terms before you rely on it. Keep both in the project's notes.

**Try it:** after the first deploy, open the logs and find the line where `migrate` runs and the line where gunicorn reports that it is listening. Write down both lines in `deploy-checklist.md`.

## 7. Check the deploy
Each deploy is a change to a live site, so check it the same way every time. Use `deploy-checklist.md` in this folder. It lists the checks before the deploy, the smoke tests after it, and the notes to keep. A smoke test is a short check that the main path works: the home page loads, the admin login works over HTTPS, the admin CSS loads, and a token login through the API returns a token.

If the admin login fails with a CSRF error on the live site, the usual cause is the proxy: check `SECURE_PROXY_SSL_HEADER` and the `DJANGO_ALLOWED_HOSTS` value, which must match the host name exactly.

**Try it:** open a page that does not exist on the live site, such as `/no-such-page/`. Read the response. It should show a plain 404 page with no traceback and no settings. Then explain which setting prevents the traceback.

## 8. After the deploy
- Rolling back: Render keeps earlier deploys. Choose the last good deploy in the dashboard, and roll back to it.
- Changing a variable restarts the service. Plan for the restart.
- The logs are the first place to look when something breaks. Read the last error before you change any code.
- Record the live URL in the project's README. The portfolio and the CV need it.

## Exit checklist
- [ ] I can list the six parts of a deployed app, and say which one each setting controls
- [ ] I can explain why `runserver` is not used in production, and why WhiteNoise is needed
- [ ] I can say what `DATABASE_URL` contains, and why SQLite is kept for local work
- [ ] I can explain why the bind address must be `0.0.0.0:$PORT`
- [ ] `pytest circles/tests/test_deployment.py` passes, all 9 tests
- [ ] The Gameya project is deployed, and `deploy-checklist.md` is filled in for it, with the live URL

## Common mistakes
- Binding gunicorn to `127.0.0.1`. Render cannot reach it.
- Leaving `DJANGO_ALLOWED_HOSTS` empty or wrong, which makes every request fail.
- Putting a secret key in `render.yaml` or in git instead of generating it on the host.
- Keeping SQLite on a server: the data disappears on the next redeploy.
- Forgetting `collectstatic`, so the admin page loads without CSS.
- Skipping the smoke test after a deploy, and finding the break from a user.
