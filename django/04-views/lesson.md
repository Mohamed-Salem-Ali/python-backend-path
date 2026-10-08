# Module 04 (Django): Views

By the end you can choose between a function view and a class-based view, handle GET and POST in one view, return JSON with the right status code, look up an object or return a 404, and validate posted data with a form.

**Before you start:** finish modules 02 (models) and 03 (forms). The views use the `Gameya`, `Member` and `Payment` models and the `PaymentForm`.

**How to read the examples:** the code here uses a made-up library app. None of it is part of Gameya. Learn the pattern here, then apply it to Gameya in `circles/views.py` and `circles/urls.py`. The library models look like this:

```python
class Book(models.Model):
    title = models.CharField(max_length=120)
    published_on = models.DateField()

class Reader(models.Model):
    name = models.CharField(max_length=80)

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, related_name="reviews")
    stars = models.PositiveSmallIntegerField()
```

## 1. A view takes a request and returns a response
A view is any callable that receives an `HttpRequest` and returns an `HttpResponse`. Django calls it when a URL matches. Module 01 used function views. This module adds class-based views, and you will see both in the same project.

```python
from django.http import JsonResponse

def health(request):                  # a function view
    return JsonResponse({"status": "ok"})
```

## 2. Function or class? Choose by the job
A function can handle several methods with an `if request.method == "POST":` check. A class gives each method its own function, so it reads better once one URL has several methods.

| Use a function view when | Use a class-based view when |
|---|---|
| the logic is one short path, or one method | one URL needs several HTTP methods (GET and POST) |
| you want to read every line at a glance | the page is a standard pattern: a list, or one object |
| it is a small utility endpoint | you want Django's generic behaviour (lookup, 404, templates) |

Neither is "better". A class groups the GET and POST logic of one resource in one place.

## 3. A class-based view dispatches by HTTP method
`View` looks at the request method and calls the method of the same name: `get()`, `post()`, `put()`, `delete()`. If the class has no method for the request, Django returns `405 Method Not Allowed` for you. Two methods are handled for you as well: `OPTIONS` returns 200 with the allowed methods, and `HEAD` runs your `get()`.

```python
from django.http import JsonResponse
from django.views import View

class BookList(View):
    def get(self, request):
        return JsonResponse([{"title": "Dune"}], safe=False)

    # No post() method, so POST returns 405 automatically.
```

In `urls.py`, a class-based view is connected with `.as_view()`:

```python
path("books/", views.BookList.as_view(), name="book_list"),
```

URL parts such as `<int:pk>` are passed to the method as keyword arguments:

```python
class BookReviews(View):
    def get(self, request, pk):          # pk comes from the URL
        ...
```

## 4. Responses: body, type and status
- `JsonResponse(data)` returns JSON with `Content-Type: application/json`. For a list, pass `safe=False`: `JsonResponse([...], safe=False)`. Without it, Django refuses to serialise a top-level list.
- `HttpResponse("text")` returns `text/html` by default. For plain text, pass `content_type="text/plain"`.
- Use the status code that says what happened:

| Code | Meaning | Use it for |
|---|---|---|
| 200 | OK | a successful read |
| 201 | Created | a successful create (POST) |
| 204 | No content | a successful delete, with no body |
| 400 | Bad request | the data was invalid |
| 404 | Not found | the object does not exist |
| 405 | Method not allowed | the URL does not accept this method |

## 5. Reading input
- **Path parameters**: `pk` in `<int:pk>` arrives as an `int`. Django converts it, and a non-number never reaches your view.
- **Query parameters**: `request.GET` holds the `?name=value` part of the URL. Read with a default: `request.GET.get("q", "")`.
- **Form data**: `request.POST` holds the body of a form-encoded POST, which is what a browser form sends. It is empty for a JSON body. This API reads form data, not JSON bodies. Never use `request.POST` directly. Pass it to a form, as section 8 shows.

## 6. Generic views: `DetailView`
A generic view does the common work for you. `DetailView` looks up one object using the URL keyword argument `pk` (or `slug`), raises a 404 if it is missing, and then renders the result. By default it renders a template. To return JSON instead, override `render_to_response()`:

```python
from django.http import JsonResponse
from django.views.generic import DetailView

class BookDetail(DetailView):
    model = Book

    def render_to_response(self, context, **response_kwargs):
        book = self.object                 # DetailView has already looked it up
        return JsonResponse({"id": book.pk, "title": book.title})
```

`self.object` is the book the URL asked for. If there is no such book, `DetailView` returns 404 before your code runs. If the URL names its keyword something else, `DetailView` cannot find the object and raises an `AttributeError`, so keep the name `pk`.

Use `DetailView` when the page is "one object"; use `View` when the logic is custom.

## 7. Looking up an object yourself: `get_object_or_404`
In a plain `View`, do the lookup with `get_object_or_404`. It returns the object, or raises a 404:

```python
from django.shortcuts import get_object_or_404

class BookReviews(View):
    def get(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        reviews = book.reviews.all()
        return JsonResponse([{"stars": r.stars} for r in reviews], safe=False)
```

Use `get_object_or_404` for every lookup you do by hand. Never call `Book.objects.get(pk=pk)` in a view: a missing book raises `DoesNotExist`, and the user sees a 500 error instead of a 404.

## 8. Validating posted data with a form
A POST view builds a form from `request.POST`, checks it, and either reports the errors or saves. Module 03 built the forms; the view is where they are used. Here are the two branches on their own.

When the data is invalid, return 400 with the errors:

```python
form = ReviewForm(data=request.POST)
if not form.is_valid():
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)
```

`form.errors.get_json_data()` keeps both the message and the code of each error. Each field maps to a list of `{"message": ..., "code": ...}` entries, and non-field errors appear under the key `"__all__"`.

When the data is valid, save and return 201:

```python
review = form.save(commit=False)     # build the Review, but do not save it yet
review.book = book                   # the form does not know the book; the URL does
review.save()
return JsonResponse({"id": review.pk, "stars": review.stars}, status=201)
```

`commit=False` lets the view add the book before the row is written.

## 9. Check what the form cannot see
The form only sees the fields that were posted. The book comes from the URL, so the form cannot compare against it. A rule about the book belongs in the view, after the form has passed. For example, inside `post()`, after `book = get_object_or_404(Book, pk=pk)`, a book cannot be reviewed before it is published:

```python
form = ReviewForm(data=request.POST)
valid = form.is_valid()
if valid and book.published_on > date.today():
    form.add_error(None, "This book is not published yet.")
    valid = False
if not valid:
    return JsonResponse({"errors": form.errors.get_json_data()}, status=400)
```

Three things to notice:
- Read `cleaned_data` only after `is_valid()`, because that is what fills it.
- `add_error(field, message)` marks the form invalid, and `None` as the field makes it a non-field error.
- After you add an error, check the result again before you save.

## 10. Avoid one query per row
A list view that loops over related objects can run one query per row. This is the N+1 problem (module 09 covers it in depth). Use `select_related` for a foreign key you will print:

```python
reviews = Review.objects.filter(book=book).select_related("reader")
```

With `select_related`, Django fetches the readers in the same query, and `review.reader.name` costs nothing extra. You can check this with `assertNumQueries` in a test.

## 11. Security: what this module does not protect
- **Anyone who gets past CSRF can write.** There is no login, so any visitor can add a review. Module 11 adds authentication and permissions.
- **CSRF.** Django returns 403 for a POST without a CSRF token. A browser form sends the token when it includes `{% csrf_token %}` (module 05). That is why `curl -X POST` gets 403 here. The Django test client skips this check by default, so the tests can POST without a token. Do not read that as "CSRF does not matter".

## 12. Habits
- Write the behaviour as a test before the view: the status code, the body and the error cases.
- One view, one resource. Keep the GET and POST of `Gameya` payments together in one class.
- Return the status that matches what happened. A 200 for an error hides the problem from the client.
- Use `get_object_or_404`, never a bare `get()`.
- Pass `request.POST` to a form; never read it field by field.

## Check your understanding
1. When would you write a function view rather than a class-based view?
2. What does Django return for a POST to a `View` that has only `get()`? Why?
3. Why does `JsonResponse` need `safe=False` for a list?
4. What does `DetailView` do before your `render_to_response()` runs?
5. A reader posts a review for a book that is not published yet, with valid stars. The form passes. Why must the view check the book's publication date?
6. Why does `get_object_or_404` matter more than `get()` for a URL like `/books/<int:pk>/`?

## Do the exercises
1. Read `circles/views.py`. Pair each view with its route, then run its test class after each pair:
   - TODO 5 (`GameyaList`) with TODO 8 (`gameya_list` route): `GameyaListTests`.
   - TODO 6 (`GameyaDetail`) with TODO 9 (`gameya_detail` route): `GameyaDetailTests`.
   - TODO 7 (`GameyaPayments`) with TODO 10 (`gameya_payments` route): `GameyaPaymentsTests`.
   Add the imports that TODO 7 needs when you write that view, not before.
2. Run `python manage.py test circles.tests.test_class_views`. Stop when all of it passes.
3. Try it by hand. Create one gameya in the admin first (module 03), so the URLs have data. Then run `python manage.py runserver` and:
   ```bash
   curl http://127.0.0.1:8000/gameyas/
   curl "http://127.0.0.1:8000/gameyas/?q=al"
   curl http://127.0.0.1:8000/gameyas/1/
   curl http://127.0.0.1:8000/gameyas/999/
   ```
   The last one should print a 404 page. Check each status with `curl -i`. On Windows PowerShell, `curl` is an alias for another command, so use `curl.exe` instead.

   Names with Arabic letters come back escaped, such as `س`. That is valid JSON, and a client decodes it. To keep the letters readable in the raw output, pass `json_dumps_params={"ensure_ascii": False}` to `JsonResponse`.

**Stretch (not tested):** add a route `gameyas/<int:pk>/payments/<int:payment_pk>/` and a class with `delete()`. Return 204 with no body. Look the payment up with `get_object_or_404(Payment, pk=payment_pk, member__gameya=gameya)`, so a payment from another gameya is a 404. Test it with the test client, because `curl -X DELETE` gets 403 until module 11.

**Project step:** the public Gameya API can be read through a browser or curl, and written through a form that sends a CSRF token. Module 05 adds HTML pages next to this JSON API.

**Done when:** all of `test_class_views` passes, and you can explain why each status code in section 4 is the right one for its case.
