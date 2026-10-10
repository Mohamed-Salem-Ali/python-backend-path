"""Module 12 acceptance tests: static files, production packages, the Render file and the database.
Do not edit.

Run (from django/gameya_site):  pytest circles/tests/test_deployment.py

They need the static root and WhiteNoise (TODO 44), the database switch (TODO 45), render.yaml
(TODO 46), and the packages in requirements.txt (TODO 47). The subprocess tests start manage.py
in a new process, with their own environment variables. gunicorn itself is not started here: it
does not run on Windows, so the tests check its configuration text instead.
"""

import os
import subprocess
import sys
from pathlib import Path

from django.conf import settings

GAMEYA_SITE = Path(__file__).resolve().parents[2]

# Long enough for Django's deploy check: at least 50 characters, and not a placeholder.
PRODUCTION_KEY = "test-only-key-" + "Qz7mR2vX9kL4pT8wB1nJ6sH3dF5gY0cA" * 2


def render_file_text():
    # Comment lines are ignored, so a TODO that mentions a setting cannot pass for the setting.
    lines = (GAMEYA_SITE / "render.yaml").read_text(encoding="utf-8").splitlines()
    return "\n".join(line for line in lines if not line.lstrip().startswith("#"))


def production_env(**extra):
    return {
        "DJANGO_PRODUCTION": "1",
        "DJANGO_SECRET_KEY": PRODUCTION_KEY,
        "DJANGO_ALLOWED_HOSTS": "gameya.example.com",
        **extra,
    }


def run_manage(*args, **env):
    # Start from a clean environment, so settings on this machine cannot leak into the test.
    clean = {
        name: value
        for name, value in os.environ.items()
        if not name.startswith("DJANGO_") and name != "DATABASE_URL"
    }
    clean.update(env)
    return subprocess.run(
        [sys.executable, "manage.py", *args],
        cwd=GAMEYA_SITE,
        env=clean,
        capture_output=True,
        text=True,
        timeout=120,
    )


# Part 1: static files. In production DEBUG is off, so Django no longer serves them. WhiteNoise
# serves them from one folder that collectstatic fills.
def test_static_files_have_a_root_folder():
    assert settings.STATIC_ROOT, "STATIC_ROOT is not set"


def test_whitenoise_serves_static_files_right_after_security():
    middleware = list(settings.MIDDLEWARE)
    security = middleware.index("django.middleware.security.SecurityMiddleware")
    assert middleware[security + 1] == "whitenoise.middleware.WhiteNoiseMiddleware"


def test_collectstatic_runs_for_production():
    result = run_manage("collectstatic", "--noinput", "--dry-run", **production_env())
    assert result.returncode == 0, result.stdout + result.stderr
    assert "static file" in result.stdout


# Part 2: the packages that production needs, pinned in requirements.txt.
def test_requirements_list_the_production_packages():
    lines = (GAMEYA_SITE / "requirements.txt").read_text(encoding="utf-8").lower().splitlines()
    for name in ("gunicorn", "whitenoise", "psycopg"):
        assert any(line.startswith(name) for line in lines), f"{name} is not in requirements.txt"


def test_the_wsgi_application_loads():
    from config.wsgi import application

    assert callable(application)


# Part 3: the Render file. It runs the migrations, then gunicorn, and asks Render to make the
# secret key, so the key is never written in the file.
def test_render_file_migrates_then_starts_gunicorn():
    text = render_file_text()
    assert "python manage.py migrate" in text
    assert "gunicorn config.wsgi:application" in text
    assert text.index("python manage.py migrate") < text.index("gunicorn config.wsgi:application")


def test_render_file_generates_the_secret_key_and_reads_the_hosts():
    text = render_file_text()
    assert "DJANGO_PRODUCTION" in text
    assert "DJANGO_SECRET_KEY" in text and "generateValue: true" in text
    assert "DJANGO_ALLOWED_HOSTS" in text
    assert "test-only-key" not in text


# Part 4: the database. A DATABASE_URL, as Render gives it, selects PostgreSQL. Without one, the
# project keeps its SQLite file for local work.
def test_database_url_selects_postgresql():
    url = "postgres://gameya:test-only-password@db.example.com:5432/gameya"
    result = run_manage(
        "shell",
        "-c",
        "from django.conf import settings as s; d = s.DATABASES['default']; "
        "print(d['ENGINE'], d['HOST'], d['NAME'])",
        **production_env(DATABASE_URL=url),
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "django.db.backends.postgresql db.example.com gameya" in result.stdout


def test_without_database_url_the_project_uses_sqlite():
    result = run_manage(
        "shell",
        "-c",
        "from django.conf import settings as s; print(s.DATABASES['default']['ENGINE'])",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "django.db.backends.sqlite3" in result.stdout
