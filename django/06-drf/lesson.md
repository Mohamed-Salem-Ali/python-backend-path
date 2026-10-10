# Module 06 (Django): Django REST Framework

By the end you can expose models as a JSON API with serializers and viewsets, route it with a router, protect writes with token authentication and a permission class, paginate and filter lists, and check the query count of an endpoint.

**Before you start:** finish modules 02 to 05. The API uses the `Gameya` and `Member` models. Module 04 built the same data by hand with plain views. This module lets DRF do the repetitive work.

**Setup (15 minutes):**
```bash
pip install "djangorestframework>=3.16,<4"
```
Add the same line to `requirements.txt`. Then, in `config/settings.py`, add `"rest_framework"` and `"rest_framework.authtoken"` to `INSTALLED_APPS` (TODO 15), and run `python manage.py migrate`. Until both apps are listed, `Token` is an abstract class and the token tests fail with `type object 'Token' has no attribute 'objects'`. The second app creates the table that stores tokens.

**How to read the examples:** the code here uses the library app from module 04: `Book`, `Reader` and `Review`. None of it is part of Gameya. Learn the pattern here, then apply it to Gameya in `circles/serializers.py` and `circles/api.py`.

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

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["book", "reader"], name="one_review_per_reader"),
        ]
```

## 1. What DRF saves you
In module 04, each view built its own dictionary and its own status codes. That works for one endpoint, but it repeats the same work everywhere, and the output can drift from the model. DRF moves the work into three pieces:

| Piece | Job | Module 04 equivalent |
|---|---|---|
| **Serializer** | converts a model to a dict, and checks incoming data | the dict built in `get()` and the `form` in `post()` |
| **Viewset** | the list, detail, create, update and delete actions for one model | one `View` class per URL |
| **Router** | builds the URLs for a viewset | the `path()` lines in `urls.py` |

## 2. Serializers: model to data, and data to model
A `ModelSerializer` reads the model and builds fields for it. List the fields you want in `Meta.fields`:

```python
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "published_on"]
```

`BookSerializer(book).data` gives a dict, ready for a JSON response.

You can also list a model property or a method with no arguments in `fields`. DRF calls it for you and makes it read-only, so no declaration is needed. A value that is neither a model field nor a property or method must be declared. A field that reads a related value uses `source`, with a dotted path:

```python
class BookSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(source="published_on.year", read_only=True)

    class Meta:
        model = Book
        fields = ["id", "title", "published_on", "year"]
```

`read_only=True` means the value goes out, but input for it is ignored. A client cannot set a computed value.

Validation on the way in works like a form (module 03). Tighten a field with a keyword argument, or write a `validate_<field>()` method. This snippet goes inside the same `BookSerializer` class, so its `Meta` stays as above:

```python
class BookSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=120, min_length=2)

    def validate_title(self, value):
        if value.strip().lower() == "untitled":
            raise serializers.ValidationError("Give the book a real title.")
        return value

    class Meta:  # as above
        model = Book
        fields = ["id", "title", "published_on"]
```

Then the view checks the data and reads the result:

```python
serializer = BookSerializer(data=request.data)
if serializer.is_valid():
    serializer.save()  # creates the Book
else:
    serializer.errors  # {"title": ["..."]}
```

The model's constraints apply too. A `UniqueConstraint` covering several fields is checked by DRF, and a duplicate comes back as a 400, not a 500. For this to happen, every field of the constraint must be a writable field of the serializer. If one is read-only, DRF skips the check and the database raises an error instead. Keep the constraint's fields writable.

## 3. Viewsets: the actions for one model
A `ModelViewSet` provides `list`, `retrieve`, `create`, `update`, `partial_update` and `destroy`. Name the queryset and the serializer, and DRF does the rest. If you want only some of the actions, use a smaller base. A read-only viewset gives you `list` and `retrieve` only:

```python
from rest_framework import viewsets


class ReaderViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Reader.objects.order_by("name")
    serializer_class = ReaderSerializer
```

A `ModelViewSet` would add the write actions. You can also combine mixins with `GenericViewSet`. Choose the smallest one that does the job.

The viewset above uses `ReaderSerializer`, which is a `ModelSerializer` for `Reader` with `fields = ["id", "name"]`, written the same way as `BookSerializer` in section 2.

## 4. Routers: the URLs for a viewset
A `DefaultRouter` builds the URLs and names them. Register each viewset with a prefix and a `basename`, then include the router under a path:

```python
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("readers", ReaderViewSet, basename="reader")

urlpatterns = [
    path("library/", include(router.urls)),
]
```

The router creates the names `reader-list` (for `/library/readers/`) and `reader-detail` (for `/library/readers/<pk>/`). It also creates an API root named `api-root` (for `/library/`), which links to each registered prefix. Tests and templates use the names, never the paths, so the URLs can change without breaking them.

## 5. Actions: an extra endpoint on one object
`@action` adds an endpoint to a viewset. With `detail=True`, it works on one object, and its URL includes the pk. This one lists the readers who reviewed a book:

```python
from rest_framework.decorators import action
from rest_framework.response import Response


class BookViewSet(viewsets.ModelViewSet):
    ...

    @action(detail=True, methods=["get"])
    def readers(self, request, pk=None):
        book = self.get_object()  # looks up the book, and returns 404 if missing
        readers = Reader.objects.filter(reviews__book=book).distinct()
        return Response(ReaderSerializer(readers, many=True).data)
```

The route is `/library/books/<pk>/readers/`, and its name is `book-readers`. `self.get_object()` does the lookup, so you do not write `get_object_or_404` yourself.

## 6. Authentication: who is calling?
DRF checks authentication before it runs the view. This module uses tokens. A token is a long random string that belongs to one user. The client sends it in a header on every request:

```text
Authorization: Token <the token string the server gave you>
```

The built-in view `obtain_auth_token` trades a username and password for a token. It creates the token the first time, and returns the same one after that:

```python
from rest_framework.authtoken.views import obtain_auth_token

(path("login/", obtain_auth_token, name="login"),)
```

A wrong password gets a 400, not a token. Set the authentication classes on the viewset, so you know exactly what is accepted:

```python
from rest_framework.authentication import TokenAuthentication


class ReaderViewSet(viewsets.ReadOnlyModelViewSet):
    authentication_classes = [TokenAuthentication]
    ...
```

Why set it? DRF's default list starts with session authentication. For an anonymous request, the first authenticator decides the status code. Token authentication gives 401, with a `WWW-Authenticate` header that tells the client how to log in. Session authentication has no such header to send, so DRF answers 403 instead. Section 7 explains the difference.

## 7. Permissions: is this user allowed?
A permission class has one job: say yes or no for this request. Subclass `BasePermission` and override `has_permission()`. `SAFE_METHODS` are the methods that only read (GET, HEAD and OPTIONS). This class lets everyone read and nobody write:

```python
from rest_framework.permissions import SAFE_METHODS, BasePermission


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
```

Two status codes come from this:
- **401 Unauthorized**: the request has no valid credentials. The client should log in and try again.
- **403 Forbidden**: the client is known, but the rule says no. Logging in again will not help.

A permission class may also define `has_object_permission()`, which checks one object. Use it when the rule depends on the object itself, such as "only the reviewer may edit this review". The learner's permission class in `api.py` also lets staff write, so read the TODO before you write it.

## 8. Pagination: one page at a time
A list of thousands of rows should not go out in one response. `PageNumberPagination` returns one page and says where the next one is:

```python
from rest_framework.pagination import PageNumberPagination


class FivePerPage(PageNumberPagination):
    page_size = 5


class ReviewViewSet(viewsets.ModelViewSet):
    pagination_class = FivePerPage
```

The response has `count`, `next`, `previous` and `results`. The client asks for another page with `?page=2`. A viewset without a pagination class returns a plain JSON list, which is what the members action in TODO 20 does on purpose.

## 9. Filtering and search: let the client narrow the list
`filter_backends` names the tools that read query parameters. Two are built in. `OrderingFilter` sorts by the fields you list:

```python
from rest_framework import filters


class ReviewViewSet(viewsets.ModelViewSet):
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["stars"]  # ?ordering=-stars
```

If `ordering_fields` is not set, DRF allows the readable serializer fields. Set it when you want to limit what a client can sort by.

For a parameter that no built-in tool handles, read it in `get_queryset()`. This one keeps reviews with at least a given number of stars:

```python
from rest_framework.exceptions import ValidationError


class ReviewViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        queryset = Review.objects.select_related("reader")
        min_stars = self.request.query_params.get("min_stars")
        if min_stars is not None:
            try:
                value = int(min_stars)
            except ValueError:
                raise ValidationError({"min_stars": "Must be a whole number."})
            if not 1 <= value <= 5:
                raise ValidationError({"min_stars": "Must be between 1 and 5."})
            queryset = queryset.filter(stars__gte=value)
        return queryset
```

Convert the value with `int()` inside `try/except ValueError`, then check its range. Do not use `isdigit()` to check it. `"²".isdigit()` is true, but `int("²")` raises an error. A very large number passes both checks and overflows the database, so check the range too. Either problem, uncaught, returns a 500. A check that returns 400 is the right behaviour here, because the client sent a bad value.

## 10. Avoid one query per row, again
A serializer that reads a related object, such as `reader.name` for each review, runs one query per row unless the queryset loads it. `select_related` in `get_queryset()` fixes that. Test it with `assertNumQueries` around the request. The count you expect depends on the request: an anonymous request runs one query for the list, and a request with a token runs one more for the user and the token.

A computed field has the same problem. If `Member.due()` reads `self.gameya.share_value`, then each member loads its gameya, unless the queryset already holds it.

A paginated list also needs an order. A queryset with no ordering gives DRF's paginator a warning (`UnorderedObjectListWarning`), because pages can then repeat or skip rows. Gameya has an order from its model's `Meta.ordering`, so the warning does not appear there.

## 11. Security: what token authentication does and does not do
- **Tokens are secrets.** Anyone with the token is that user. Send it only over HTTPS (module 12 covers deployment). Never put it in a URL, because URLs are logged.
- **Tokens do not expire by default.** To end a session, delete the token: `Token.objects.filter(user=request.user).delete()`.
- **CSRF does not apply to token requests**, because the browser does not send the token on its own. Session authentication does need CSRF protection, which is one reason to choose tokens for an API used by programs.
- **Login is only part of the story.** Module 11 covers sessions versus JWT, CSRF, secure settings and ownership permissions.

## 12. Habits
- Write the serializer first, with its tests: the fields, the read-only fields, and each validation rule.
- Set `authentication_classes` and `permission_classes` on every viewset. Do not rely on the defaults.
- Return the status code that tells the client what to do next: 401 to log in, 403 to stop, 400 to fix the input.
- Validate every query parameter before you use it.
- Test the query count of every list endpoint.

## Check your understanding
1. What does a `ModelSerializer` produce on output, and what does `is_valid()` check on input?
2. Why is a `read_only` field ignored on input, and what does `source="published_on.year"` read?
3. A client sends a second review for the same `(book, reader)` pair. Which layer returns the 400, and why must both fields be writable in the serializer?
4. What does `ReadOnlyModelViewSet` give you, and what does the router add on top of it?
5. An anonymous client sends a POST to a viewset with `TokenAuthentication`. Which status code does it get, and why would session authentication give a different one?
6. Why does `?min_stars=abc` need a check inside `get_queryset()`, and why is `isdigit()` not enough?
7. A list endpoint runs 1 query for the list and 1 query per row for a related field. What single change in `get_queryset()` fixes it?

## Do the exercises
1. **Setup.** Install DRF and add it to `requirements.txt`. Add the two apps to `INSTALLED_APPS` (TODO 15), and run `python manage.py migrate`. Then run `python manage.py test circles.tests.test_api.SetupTests`. It should pass.
2. **Serializers.** Write `GameyaSerializer` (TODO 16) and `MemberSerializer` (TODO 17). Run `python manage.py test circles.tests.test_api.ApiStructureTests.test_turns_payout_and_weekly_pot_are_read_only`. That test passes now. The other test in the class needs the viewsets, so it passes after step 4.
3. **Permission and pagination.** Write the permission class (TODO 18) and the page-size class (TODO 19). Nothing runs on its own yet, so go on to step 4.
4. **Viewsets.** Write `GameyaViewSet` (TODO 20) and `MemberViewSet` (TODO 21). Each one uses the classes from steps 2 and 3.
5. **Routes.** Only after step 4, register both viewsets with a `DefaultRouter`, and add the token route (TODO 22). Do not do this earlier. `register()` runs when `urls.py` loads. If the viewsets do not exist yet, the whole project fails to start, and every test in every module fails with it.
6. **Run the module.** Run `python manage.py test circles.tests.test_api`. Stop when all 33 tests pass.
7. **Try it by hand.** Create a staff user with `python manage.py createsuperuser`. Start the server in a second terminal with `python manage.py runserver`. Then, in PowerShell (Windows), run these in order:
   ```powershell
   curl.exe -X POST http://127.0.0.1:8000/api/token/ -d "username=YOURNAME&password=YOURPASSWORD"
   curl.exe -H "Authorization: Token PASTE_THE_TOKEN" http://127.0.0.1:8000/api/gameyas/
   curl.exe -i -X POST http://127.0.0.1:8000/api/gameyas/ -d "name=X&weeks=2&share_value=10&start_date=2026-11-01"
   ```
   The second command sends the token, so it returns the list. The third sends no token, and writing needs one. It should print a 401 with a `WWW-Authenticate` header. Reading needs no token, so `curl.exe http://127.0.0.1:8000/api/gameyas/` works without one. Also open `http://127.0.0.1:8000/api/` in a browser to see the API root.

**Stretch (not tested):** add a `ReviewSerializer` with `book`, `reader` and `stars` fields, and a `ReviewViewSet` that uses it. Check that a second review for the same `(book, reader)` pair returns a 400.

**Project step:** the Gameya data is now a JSON API that clients can read, and that staff can change with a token. Module 07 (middleware and signals) and module 08 (testing in Django) build on this.

**Done when:** all of `test_api` passes, and you can explain why each of the three status codes 400, 401 and 403 is right for its case.
