# Module 05 (Django): Templates

By the end you can render HTML pages from views with the Django template language, reuse one layout across pages with inheritance, show data safely (Django escapes it for you), load static files, and show a list page with a fallback when it is empty.

**Before you start:** finish modules 02 to 04. The pages use the `Gameya` and `Member` models and the class-based views.

**How to read the examples:** the code here uses a made-up library app (`Book`, `Author`). None of it is part of Gameya. Learn the pattern here, then apply it to Gameya in `circles/views.py`, `circles/urls.py` and the templates you create under `circles/templates/circles/`.

## 1. Templates keep HTML out of Python
A view decides which data a page needs. A template decides how to show it. Keep the HTML in a template file and the logic in the view:

```python
from django.shortcuts import render

def book_list(request):
    books = Book.objects.order_by("title")
    return render(request, "books/book_list.html", {"books": books})
```

`render()` loads the template, fills in the context dictionary, and returns an `HttpResponse`. Module 04 returned JSON; a template returns HTML.

## 2. Where templates live
Django looks for templates in each installed app's `templates/` folder (because `APP_DIRS` is on in `config/settings.py`). Put each app's templates under a folder named after the app, so two apps can each have a `base.html` without clashing:

```text
circles/
  templates/
    circles/
      base.html
      home.html
```

The name you pass to `render()` is the path under `templates/`: `"circles/home.html"`.

## 3. Variables and dots
`{{ ... }}` prints a value. A dot reaches inside it: attributes, dictionary keys, list indexes, and methods that take no arguments (written without parentheses):

```html
<h1>{{ book.title }}</h1>
<p>Written by {{ book.author.name }}</p>
<p>Costs {{ book.price_in_cents }} cents</p>
```

The template does not call `book.price_in_cents()`; it calls the method for you if it takes no arguments. Anything that needs an argument must be computed in the view.

## 4. Filters change how a value shows
A filter follows a `|`. Chain them from left to right:

| Filter | Example | Result for `"dune"` |
|---|---|---|
| `title` | `{{ name\|title }}` | `Dune` |
| `upper` | `{{ name\|upper }}` | `DUNE` |
| `length` | `{{ books\|length }}` | number of items |
| `default` | `{{ book.isbn\|default:"none" }}` | `none` if empty |
| `date` | `{{ book.published\|date:"Y" }}` | `1965` |
| `pluralize` | `{{ count }} book{{ count\|pluralize }}` | `2 books` |

Filters only change what is shown. They do not change the stored data.

## 5. Tags: `if`, `for`, `url`
Tags do the work of Python statements. A `for` loop can show a message when the list is empty:

```html
<ul>
  {% for book in books %}
    <li><a href="{% url 'book_detail' book.pk %}">{{ book.title }}</a></li>
  {% empty %}
    <li>No books yet.</li>
  {% endfor %}
</ul>
```

- `{% url 'name' arg %}` builds a link from a URL name. Never type a path by hand: if the URL changes, the link follows.
- `forloop.counter` gives the position, starting from 1.
- `{% if %}` checks a condition: `{% if book.available %}...{% else %}...{% endif %}`.

## 6. Autoescaping keeps you safe
Django escapes every `{{ value }}` for you. A book title such as `<script>...</script>` shows as text, not as code:

```text
Input:   <script>alert(1)</script>
Output:  &lt;script&gt;alert(1)&lt;/script&gt;
```

This protects against cross-site scripting (XSS). Keep it that way. Do not mark a value `|safe` unless you wrote that HTML yourself, and never mark user input as safe. The tests in this module check that a member's name with HTML in it is escaped.

## 7. Inheritance: one layout for every page
A base template holds the shell of the page (head, navigation, footer). Each page extends it and fills in named **blocks**:

```html
<!-- circles/base.html -->
<!doctype html>
<html lang="en">
<head>
  <title>{% block title %}Gameya{% endblock %}</title>
</head>
<body>
  <nav><a href="{% url 'home' %}">Home</a></nav>
  <main>{% block content %}{% endblock %}</main>
</body>
</html>
```

```html
<!-- circles/book_list.html -->
{% extends "circles/base.html" %}

{% block title %}Books{% endblock %}

{% block content %}
  <h1>Books</h1>
  ...
{% endblock %}
```

Only what is inside a block replaces the base. To keep the base's content and add to it, use `{{ block.super }}` inside the child block.

## 8. Static files: CSS, images and scripts
Static files are the files a page loads but does not generate: CSS, images, JavaScript. Put them in `static/<app>/` inside the app, then load them with the `static` tag:

```html
{% load static %}
<link rel="stylesheet" href="{% static 'circles/site.css' %}">
```

With `STATIC_URL = "static/"` in settings, this becomes `/static/circles/site.css`. Django serves static files during development. Module 12 covers `collectstatic` for production.

## 9. Class-based views and templates
A generic view knows its template and its context. You can set them on the class:

```python
from django.views.generic import DetailView, ListView

class BookList(ListView):
    model = Book
    template_name = "books/book_list.html"        # the page to render
    context_object_name = "books"                  # the name the template uses

class BookDetail(DetailView):
    model = Book
    template_name = "books/book_detail.html"       # the object is "object" and "book"
```

`ListView` puts the list in the context under `object_list` and under `book_list` (the lowercase model name plus `_list`). If you set `context_object_name`, that name is used instead of `book_list`. `DetailView` puts the object under `object` and under the lowercase model name, here `book`.

To add data for the template, override `get_context_data()`:

```python
class BookDetail(DetailView):
    model = Book
    template_name = "books/book_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = self.object.reviews.order_by("-created")
        return context
```

Always call `super()` first, so the object and the other context stay in place.

## 10. Forms in templates
A form in a template needs a CSRF token, or Django rejects the POST with a 403:

```html
<form method="post">
  {% csrf_token %}
  {{ form.as_p }}
  <button type="submit">Save</button>
</form>
```

`form.as_p` renders every field with its label and errors. To style each field yourself, loop over the fields and show `field.errors` next to each one. Module 11 covers CSRF in depth.

## 11. Logic belongs in Python
Templates can compare and loop, but they should not do real work. Prefer:
- a model method or property for a figure, such as `member.due()`, over arithmetic in the template;
- a view that sorts and filters, over `{% for %}` with `{% if %}` that hides rows.

If you find yourself writing a long `{% if %}` chain, move it to the view.

## 12. Habits
- Write the test first: the template used, the text shown, and the escaping.
- Extend the base for every page. A page that does not extend it will drift from the others.
- Use `{% url %}` for every link.
- Put names in a plain `{% empty %}` message, so an empty list still looks finished.
- Check the page in a browser after each change. A test checks the HTML, not how it looks.

## Check your understanding
1. What does `render()` return, and what does it need?
2. Why do templates live in `circles/templates/circles/`, not just in `templates/`?
3. What does `{{ book.due }}` do if `due` is a method with no arguments?
4. Why does `<script>` in a member's name show as text, and when would that protection not apply?
5. A child template defines `{% block content %}`. What appears if the base has text in its own `content` block and the child does not define it?
6. What does `ListView` put in the context by default, and how do you change its name?

## Do the exercises
1. Create the base template `circles/templates/circles/base.html`. It needs a `title` block, a `content` block, a link to home built with `{% url %}`, and the stylesheet from `{% static %}`.
2. Change `circles/templates/circles/about.html` (from module 01) so it extends the base. Its content must still say "About Gameya".
3. Read `circles/views.py`, TODO 11 and 12. Write the home page as a `ListView` and the gameya page as a `DetailView` that adds the members to the context. Connect both in `circles/urls.py` (TODO 13 and 14).
4. Write `circles/templates/circles/home.html` and `circles/templates/circles/gameya_detail.html`. The home page links each gameya to its page and shows "No gameyas yet." when empty. The page shows the figures, a members table with each weekly due, and "No members yet." when empty.
5. Create `circles/static/circles/site.css`, with at least one rule, and link it from the base.
6. Run `python manage.py test circles.tests.test_templates` after each step. Stop when all tests pass.

**Stretch (not tested):** add a `{% if %}` on the members table, so a member with no shares shows "Inactive" instead of a due. Put the check in a model method, not in the template.

**Project step:** the public Gameya pages now show real data. Module 06 (DRF) gives the same data a machine-readable API.

**Done when:** all of `test_templates` passes, and you can explain how `{% extends %}` and `{% block %}` decide what a page contains.
