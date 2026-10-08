# Module 05 (Django): Templates

By the end you can render HTML pages from views with the Django template language, reuse one layout across pages with inheritance, show data safely (Django escapes it for you), load static files, and show a list with a fallback when it is empty.

**Before you start:** finish module 02 (models) and module 01 (the `about` page). The pages use the `Gameya` and `Member` models. Module 04's JSON views stay as they are; this module adds HTML views next to them.

**How to read the examples:** the code here uses the made-up library app from module 04: `Book`, `Reader` and `Review`, in an app called `library`. None of it is part of Gameya. Learn the pattern here, then apply it to Gameya in `circles/views.py`, `circles/urls.py` and the templates under `circles/templates/circles/`.

```python
class Book(models.Model):
    title = models.CharField(max_length=120)
    published_on = models.DateField()

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    stars = models.PositiveSmallIntegerField()
```

## 1. Templates keep HTML out of Python
A view decides which data a page needs. A template decides how to show it. Keep the HTML in a template file and the logic in the view:

```python
from django.shortcuts import render

def book_list(request):
    books = Book.objects.order_by("title")
    return render(request, "library/book_list.html", {"books": books})
```

`render()` loads the template, fills it with the **context** (the dictionary of data the template can use), and returns an `HttpResponse`. Module 04 returned JSON; a template returns HTML.

## 2. Where templates live
Django looks for templates in each installed app's `templates/` folder (because `APP_DIRS` is on in `config/settings.py`). Put each app's templates under a folder named after the app, so two apps can each have a `base.html` without clashing:

```text
library/
  templates/
    library/
      base.html
      book_list.html
```

The name you pass to `render()` is the path under `templates/`: `"library/book_list.html"`.

## 3. Variables and dots
`{{ ... }}` prints a value. A dot reaches inside it: attributes, dictionary keys, list indexes, and methods that take no arguments (written without parentheses):

```html
<h1>{{ book.title }}</h1>
<p>Published in {{ book.published_on|date:"Y" }}</p>
<p>Costs {{ book.price_in_cents }} cents</p>
```

Write `book.price_in_cents`, not `book.price_in_cents()`. Django calls the method for you, but only when it needs no arguments. A method that needs arguments cannot be called from a template, and it renders as nothing, with no error. Compute its result in the view instead.

A name that does not exist renders as nothing, with no error. `{{ book.nope }}` shows an empty string. This is the most common silent bug: a wrong name in a view's context makes a `{% for %}` loop take its `{% empty %}` branch, and the page looks like it has no data. Check the name first.

## 4. Filters change how a value shows
A filter follows a `|`. Chain them from left to right:

| Filter | Example | Result |
|---|---|---|
| `title` | `{{ name\|title }}` for `dune` | `Dune` |
| `upper` | `{{ name\|upper }}` for `dune` | `DUNE` |
| `length` | `{{ books\|length }}` | number of items |
| `default` | `{{ book.isbn\|default:"none" }}` | `none` if the value is false or empty, including `0` |
| `date` | `{{ book.published_on\|date:"Y" }}` | `1965` |
| `pluralize` | `{{ count }} book{{ count\|pluralize }}` | `2 books`, or `1 book` |

Filters only change what is shown. They do not change the stored data.

## 5. Tags: `if`, `for`, `url`
Tags do the work of Python statements. A `for` loop can show a message when the list is empty:

```html
<table>
  {% for review in reviews %}
    <tr>
      <td>{{ forloop.counter }}</td>
      <td>{{ review.stars }} stars</td>
    </tr>
  {% empty %}
    <tr><td>Nothing here yet.</td></tr>
  {% endfor %}
</table>
```

- `{% url 'name' arg %}` builds a link from a URL name. Never type a path by hand: if the URL changes, the link follows.
- `forloop.counter` gives the position, starting from 1.
- `{% if %}` checks a condition: `{% if book.published_on %}...{% else %}...{% endif %}`.

## 6. Autoescaping keeps you safe
Django escapes every `{{ value }}` for you. A book title such as `<script>...</script>` shows as text, not as code:

```text
Input:   <script>alert(1)</script>
Output:  &lt;script&gt;alert(1)&lt;/script&gt;
```

This protects text and quoted attributes. It does not make a URL in `href="{{ url }}"` safe, or make text inside a `<script>` block safe. Module 11 covers those cases.

Escaping is switched off in three places: a value marked `|safe`, a string returned by `mark_safe()`, and a block wrapped in `{% autoescape off %}`. Use them only for HTML you wrote yourself, and never for user input. The tests in this module check that a member's name with HTML in it is escaped.

## 7. Inheritance: one layout for every page
A base template holds the shell of the page. Each page extends it and fills in named **blocks**. Here is the part of a base template that holds the blocks:

```html
<title>{% block title %}Library{% endblock %}</title>
<main>{% block content %}{% endblock %}</main>
```

A child template extends the base and fills the blocks:

```html
{% extends "library/base.html" %}

{% block title %}Books{% endblock %}

{% block content %}
  <h1>Books</h1>
  ...
{% endblock %}
```

Two rules matter here:
- `{% extends %}` must be the first tag in the child. Text such as an HTML comment may come before it.
- In a child template, anything outside a block is ignored. Only the blocks change the page.

If the child does not define a block, the base's content inside that block shows. To keep the base's content and add to it, write `{{ block.super }}` inside the child block.

## 8. Static files: CSS, images and scripts
Static files are the files a page loads but does not generate: CSS, images, JavaScript. Put them in `static/<app>/` inside the app, then load them with the `static` tag. Each template must load the tag itself, because `{% load %}` is not inherited from the base:

```html
{% load static %}
<link rel="stylesheet" href="{% static 'library/print.css' %}">
```

With `STATIC_URL = "static/"` in settings, this becomes `/static/library/print.css`. During development, `runserver` serves static files only when `DEBUG` is on (the default here), or when you start it with `--insecure`. Module 12 covers `collectstatic` for production.

## 9. Class-based views and templates
A generic view knows its template and its context. You can set them on the class:

```python
from django.views.generic import DetailView, ListView

class BookList(ListView):
    model = Book
    template_name = "library/book_list.html"       # the page to render
    context_object_name = "books"                   # the name the template uses

class BookDetail(DetailView):
    model = Book
    # The object is in the context as "object" and as "book".
    template_name = "library/book_detail.html"
```

`ListView` puts the list in the context under `object_list` and under `book_list` (the lowercase model name plus `_list`). If you set `context_object_name`, that name is used instead of `book_list`. `DetailView` puts the object under `object` and under the lowercase model name, here `book`.

To add data for the template, override `get_context_data()`:

```python
class BookDetail(DetailView):
    model = Book
    template_name = "library/book_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["other_books"] = Book.objects.exclude(pk=self.object.pk)[:3]
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

`form.as_p` renders every field with its label, input, help text and errors. To style each field yourself, loop over the fields and show the errors next to each one:

```html
{% for field in form %}
  <p>{{ field.label_tag }} {{ field }}</p>
  {{ field.errors }}
{% endfor %}
```

Module 11 covers CSRF in depth.

## 11. Logic belongs in Python
Templates can compare and loop, but they should not do real work. Prefer:
- a model method or property for a figure, such as `book.is_recent()`, over arithmetic in the template;
- a view that sorts and filters, over a `{% for %}` with an `{% if %}` that hides rows.

If you find yourself writing a long `{% if %}` chain, move it to the view or the model.

## 12. Habits
- Write the test first: the template used, the text shown, and the escaping.
- Extend the base for every page. A page that does not extend it will drift from the others.
- Use `{% url %}` for every link.
- Give every list a plain `{% empty %}` message, so an empty list still looks finished.
- Check the page in a browser after each change. A test checks the HTML, not how it looks.

## Check your understanding
1. What does `render()` return, and what does it need?
2. Why do templates live in `library/templates/library/`, not just in `templates/`?
3. In a template, why does `{{ book.price_in_cents }}` work with no parentheses, and what happens if the method needs an argument?
4. A member's name is `<script>alert(1)</script>`, and the template prints `{{ name }}`. Why does it show as text? Name two places where that protection is switched off.
5. A base template has text inside `{% block content %}`. A child template extends it but does not define a `content` block. What appears on the page?
6. What does `ListView` put in the context by default, and how do you change its name?
7. A view puts `books` in the context, but the template loops over `{% for b in book_list %}`. What does the user see, and why is there no error?

## Do the exercises
1. Create the base template `circles/templates/circles/base.html`. It needs the same three parts as the library base in sections 7 and 8: a `title` block, a `content` block, a link to home built with `{% url %}`, and the stylesheet loaded with `{% static %}`.
2. Change `circles/templates/circles/about.html`, from module 01, so it extends the base. Its content must still say "About Gameya".
3. Read `circles/views.py`. Pair each view with its route, then run its test class after each pair:
   - TODO 11 (`GameyaHome`) with TODO 13 (the `home` route): `HomePageTests`.
   - TODO 12 (`GameyaPage`) with TODO 14 (the `gameya_page` route): `GameyaPageTests`.
4. Write `circles/templates/circles/home.html` and `circles/templates/circles/gameya_detail.html`. The home page links each gameya to its page and shows "No gameyas yet." when the list is empty. The gameya page shows the payout and the weekly pot, a members table with each member's weekly due, and "No members yet." when empty.
5. Create `circles/static/circles/site.css` with at least one rule, and link it from the base.
6. Run `python manage.py test circles.tests.test_templates` at the end. Stop when all 20 tests pass.
7. Check it in a browser. In the admin, create a gameya with two members. Run `python manage.py runserver`, then open `/` and `/gameyas/<id>/page/`. The stylesheet should change the page, and the page should list both members with their dues.

**Stretch (not tested):** add `is_active()` to `Member`. It returns `False` when `shares` is 0. In the members table, show "Inactive" instead of a due when `{% if member.is_active %}` is false. Shares can be 0 in the admin, so you can try it by hand.

**Project step:** the public Gameya pages show real data. Module 06 (DRF) rebuilds a JSON API like the one from module 04, with serializers and viewsets, so you can compare the two.

**Done when:** all of `test_templates` passes, and you can explain how `{% extends %}` and `{% block %}` decide what a page contains.
