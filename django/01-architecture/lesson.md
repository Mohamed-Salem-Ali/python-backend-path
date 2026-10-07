# Module 01 (Django): Architecture

By the end you can explain how a Django request becomes a response, set up a project and an app, route URLs to views, and render a template.

## 1. What Django is
Django is a "batteries included" web framework: URL routing, an ORM (database layer), templates, forms, authentication, an admin site, security protections, migrations and a test runner, all designed to work together. You give up some freedom and get a lot of speed and consistency. It is the right tool when you want a real application with a database, users and an admin in days, not weeks.

## 2. MTV: Model, Template, View
Django calls its pattern **MTV**, close to the MVC you may have heard of:

| Django | Role | Example |
|---|---|---|
| **Model** | Data and rules, mapped to a database table | `Gameya`, `Member`, `Payment` |
| **Template** | The HTML shown to the user | `about.html` |
| **View** | The code that handles a request and returns a response | `def about(request): ...` |

(Django itself plays the "controller": it routes each URL to the right view.)

## 3. The request/response cycle
This is the most important diagram to hold in your head:

```text
Browser ──HTTP request──▶ web server (runserver / gunicorn)
                              │
                              ▼
                         WSGI / ASGI
                              │
                              ▼
                  Middleware (in order, going in)
                              │
                              ▼
          URLconf: match the path to a view   ── no match ──▶ 404
                              │
                              ▼
                 View(request, *args) ──▶ may use Models (database)
                              │          and Templates (HTML)
                              ▼
                       HttpResponse
                              │
                  Middleware (in reverse order, going out)
                              ▼
Browser ◀────HTTP response────┘
```
Every page, API endpoint and admin screen follows this path. When something breaks, ask: "which step is it in?"

## 4. Project vs app
- A **project** is the whole website: settings, root URLs, and the entry points. You have one.
- An **app** is one self-contained feature (circles, payments, accounts). A project has several. An app can be reused in other projects.

In this repo: the project is `config/` (settings and root URLs) and the app is `circles/`. Everything lives under `django/gameya_site/`.

## 5. Look at what Django generates
Once, in a throwaway folder (not in this repo), run:
```bash
python -m venv .venv && .venv\Scripts\Activate.ps1
pip install "Django>=5.2,<5.3"
django-admin startproject config .
python manage.py startapp circles
```
You get:
```text
manage.py            the command-line tool for everything: runserver, migrate, test, shell...
config/
    settings.py      all configuration
    urls.py          the root URLconf
    asgi.py, wsgi.py entry points for servers
circles/
    models.py        data
    views.py         request handlers
    admin.py         admin registrations
    apps.py          app configuration
    migrations/      the history of database changes
    tests.py         tests (we use a tests/ package instead)
```
Delete the folder afterwards. The repo's `django/gameya_site/` is already set up this way.

## 6. Run it
```bash
cd django/gameya_site
python -m venv .venv
.venv\Scripts\Activate.ps1            # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py check                # find configuration mistakes
python manage.py migrate              # create the database tables (first time)
python manage.py runserver            # http://127.0.0.1:8000/
```
`runserver` reloads when you save a file. It is for development only; production uses gunicorn (Week 9). `python manage.py createsuperuser` makes an admin user for `/admin/` (Week 6).

## 7. Settings, explained
Open `config/settings.py` and read every comment. The ones that matter most:
- `SECRET_KEY`: signs sessions and tokens. **Secret.** Read from the environment in production.
- `DEBUG`: shows detailed error pages. **Must be off in production.**
- `ALLOWED_HOSTS`: host names the site may serve; required when `DEBUG` is off.
- `INSTALLED_APPS`: every app Django should load (ours is `circles`). Forgetting this is the classic "my model/template is ignored" bug.
- `MIDDLEWARE`: the ordered layers around every request (security, sessions, CSRF, authentication...).
- `TEMPLATES`: where and how templates are found (`APP_DIRS: True` means `templates/` inside each app).
- `DATABASES`: SQLite for now; PostgreSQL later.
- `TIME_ZONE`, `USE_TZ`: store datetimes in UTC (`USE_TZ = True`), display in `Africa/Cairo`.

Environment-based settings (`os.environ.get(...)`) keep secrets out of Git.

## 8. URL routing
The root `config/urls.py` delegates to each app:
```python
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("circles.urls")),
]
```
The app's `circles/urls.py` maps paths to views:
```python
from django.urls import path
from . import views

urlpatterns = [
    path("health/", views.health, name="health"),
    path("hello/<str:name>/", views.hello, name="hello"),
    path("add/<int:a>/<int:b>/", views.add, name="add"),
]
```
- **Converters** capture and convert parts of the path: `<str:name>` (any text without `/`), `<int:id>` (digits, passed as `int`), `<slug:slug>`, `<uuid:id>`. A path that does not match, such as `/add/x/2/`, is a 404.
- **Names** let you build URLs without hard-coding them: `reverse("hello", args=["Sara"])` gives `/hello/Sara/`, and `{% url "hello" "Sara" %}` does the same in templates. Rename a path later and nothing breaks.
- Patterns are tried **in order**; the first match wins.

## 9. Views
A view is a function that takes an `HttpRequest` and returns an `HttpResponse`.
```python
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET


def hello(request, name):  # `name` comes from the URL converter
    return HttpResponse(f"Hello, {name}!")


@require_GET  # a decorator (Module 10): other methods get 405
def health(request):
    return JsonResponse({"status": "ok"})


def about(request):
    return render(request, "circles/about.html", {"title": "About Gameya"})
```
Useful request attributes: `request.method`, `request.GET` (query string), `request.POST` (form data), `request.headers`, `request.user`, `request.path`. Useful responses: `HttpResponse`, `JsonResponse`, `render`, `redirect`, `Http404`.

## 10. Templates
HTML files with placeholders and a small language:
```html
<!doctype html>
<html>
  <head><title>{{ title }}</title></head>
  <body>
    <h1>{{ title }}</h1>                       {# a variable #}
    {% for member in members %}                {# a tag: logic #}
      <p>{{ member.name|upper }}</p>           {# a filter #}
    {% empty %}
      <p>No members yet.</p>
    {% endfor %}
    {% if user.is_authenticated %}...{% endif %}
    <a href="{% url 'about' %}">About</a>
  </body>
</html>
```
- `{{ variable }}` is **auto-escaped**: `<script>` becomes `&lt;script&gt;`, which is Django's first defence against XSS. Do not use `|safe` on user input.
- Template **inheritance** shares a layout: a `base.html` with `{% block content %}{% endblock %}`, and pages that `{% extends "base.html" %}` and fill the block.
- Templates live in `circles/templates/circles/` (the repeated app name prevents clashes between apps).

## 11. Talking to the shell
```bash
python manage.py shell
>>> from django.urls import reverse
>>> reverse("about")
'/about/'
```
The shell has your whole project loaded. Use it constantly to try ideas.

## 12. Common mistakes
- Forgetting the trailing slash in `path("health/", ...)` and visiting `/health`.
- Forgetting to add the app to `INSTALLED_APPS`.
- Putting templates in the wrong folder (`circles/templates/about.html` instead of `circles/templates/circles/about.html`).
- Returning a string or `None` from a view instead of an `HttpResponse`.
- Committing `db.sqlite3`, `.env` files or a real `SECRET_KEY`.

## Check your understanding
1. Walk through what happens between typing `/hello/Sara/` and seeing the page, naming each layer.
2. What is the difference between a project and an app?
3. What do the `SECRET_KEY`, `DEBUG` and `INSTALLED_APPS` settings do, and which two are dangerous to get wrong in production?
4. Why give URL patterns names? How do you use them in Python and in a template?
5. What does `<int:a>` do, and what happens to `/add/x/2/`?
6. What does template auto-escaping protect against?

## Do the exercises
The wiring is already there. You write the views, URLs and one template.
1. Read `circles/tests/test_architecture.py` (it is the specification).
2. Run `python manage.py test circles.tests.test_architecture`. The three "wiring" tests pass; the rest fail.
3. Fill in `circles/views.py` (four views), `circles/urls.py` (four named routes) and create `circles/templates/circles/about.html`. Run the tests after each step until they all pass.
4. Open `runserver` and visit each page in the browser, too.
