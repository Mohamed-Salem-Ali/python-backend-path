"""Django settings for the Gameya learning project.

Every setting here is explained in django/01-architecture/lesson.md. Read it once, top to bottom.
Reference: https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import os
from pathlib import Path

# The folder that contains manage.py. Build other paths from it: BASE_DIR / "templates".
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY: in production the key comes from the environment and is never committed.
# This development fallback is deliberately obvious so nobody mistakes it for a real secret.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-only-not-a-secret")

# SECURITY: never run with DEBUG on in production. Default to on for local learning.
DEBUG = os.environ.get("DJANGO_DEBUG", "1") == "1"

ALLOWED_HOSTS = [h for h in os.environ.get("DJANGO_ALLOWED_HOSTS", "").split(",") if h]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # TODO 15 (module 06): add "rest_framework" and "rest_framework.authtoken" here, above
    # "circles". Then run `python manage.py migrate`, so the token table exists.
    "circles",  # our app
]

MIDDLEWARE = [
    # TODO 27 (module 07): add "circles.middleware.RequestIdMiddleware" as the first entry.
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,  # look for templates/ inside each installed app
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# SQLite is perfect for learning: a single file, no server. Week 9 switches to PostgreSQL.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Cairo"
USE_I18N = True
USE_TZ = True  # store datetimes in UTC, convert to TIME_ZONE for display

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# TODO 34 (module 09): add a CACHES setting with one entry named "default": the in-memory
#          backend (LocMemCache), a LOCATION name of your choice, and a TIMEOUT of 300 seconds.
#          Django uses LocMemCache even without this setting. Writing it down makes the choice
#          and the timeout visible. A production setup can switch the backend to Redis.

# TODO 37 (module 10): the Celery settings. Give each one a value, in this order:
#   CELERY_BROKER_URL: the broker's address, read from the environment variable
#                      CELERY_BROKER_URL, with "memory://" as the default. The lesson explains
#                      what a broker is and why memory is fine for learning.
#   CELERY_TASK_ALWAYS_EAGER: True unless the environment variable CELERY_EAGER is set to "0".
#                      Eager tasks run in the same process, right away. Tests need this.
#   CELERY_TASK_EAGER_PROPAGATES: False. An eager task that fails does not raise at once: its
#                      .get() raises the error instead. With True, a retry escapes as a Retry
#                      signal before it runs, so the retry tests could not see it.
#   CELERY_BEAT_SCHEDULE: one entry that runs circles.tasks.queue_unpaid_reports every day at
#                      08:00. Use celery.schedules.crontab for the time. The key of the entry
#                      is a name you choose.
#   GAMEYA_ORGANISER_EMAIL: the address that receives the reports, read from the environment
#                      variable GAMEYA_ORGANISER_EMAIL, with "organiser@example.com" as the default.
#   EMAIL_BACKEND: the console backend, so emails print in the terminal during local work. Django
#                      sends real mail by default, which fails here without a mail server. The
#                      tests collect emails in memory instead, so they do not use this setting.

# TODO 42 (module 11): the JWT settings. Add a dictionary named SIMPLE_JWT, with three entries:
#   ACCESS_TOKEN_LIFETIME: 15 minutes, as a timedelta. Access tokens are short-lived on purpose.
#   REFRESH_TOKEN_LIFETIME: 7 days.
#   AUTH_HEADER_TYPES: ("Bearer",), the word before the token in the Authorization header.
#          Import timedelta from datetime at the top of this file.
# TODO 43 (module 11): production settings, switched on by the environment variable
#          DJANGO_PRODUCTION set to "1". Section 7 of the lesson explains each one.
#   1. PRODUCTION = os.environ.get("DJANGO_PRODUCTION") == "1", above SECRET_KEY.
#   2. SECRET_KEY: production has no fallback. Without DJANGO_SECRET_KEY, raise
#      ImproperlyConfigured (from django.core.exceptions), with a message that names the variable.
#      Keep a development fallback for local work, at least 32 characters long, because the JWT
#      signature uses this key.
#   3. DEBUG: never on in production.
#   4. When PRODUCTION is set: SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https"),
#      SECURE_SSL_REDIRECT, SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE, SECURE_HSTS_SECONDS = 3600,
#      and SECURE_HSTS_INCLUDE_SUBDOMAINS and SECURE_HSTS_PRELOAD, both True.
#   Then run `python manage.py check --deploy` with DJANGO_PRODUCTION=1 and a long key.

# TODO 44 (module 12): static files, served by WhiteNoise. Section 3 of the module 12 lesson.
#   1. STATIC_ROOT: a folder named "staticfiles" inside BASE_DIR. collectstatic copies every static
#      file there, and WhiteNoise serves them from there.
#   2. MIDDLEWARE: add "whitenoise.middleware.WhiteNoiseMiddleware" directly after
#      "django.middleware.security.SecurityMiddleware". The order matters: it must run early.

# TODO 45 (module 12): the database. Section 4 of the module 12 lesson.
#   Keep the SQLite entry in DATABASES for local work. When the environment variable DATABASE_URL
#   is set, use PostgreSQL instead. Read the URL with urllib.parse.urlparse (import it at the top).
#   Fill in ENGINE "django.db.backends.postgresql", NAME (the path without its leading slash),
#   USER, PASSWORD, HOST, and PORT (use 5432 when the URL has none).
