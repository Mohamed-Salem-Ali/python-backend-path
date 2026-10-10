# Module 03 (Django): Admin and forms

By the end you can register models in the Django admin and shape their pages, and you can write forms that check user input before it reaches your database: from a model with `ModelForm`, and from scratch with `forms.Form`.

**Before you start:** finish module 02. The admin and forms work on the `Gameya`, `Member`, `Payment` and `PayoutSlot` models.

**How to read the examples:** the code in this lesson uses a made-up library app (`Author`, `Book`) and a booking form. None of it is part of Gameya. Learn the pattern here, then apply it to Gameya in `circles/admin.py` and `circles/forms.py`.

## 1. The admin is a back office you get for free
Django's admin is a web interface generated from your models. It gives you lists, search, filters, and add and edit pages, with no templates to write. Two lines connect it to your project, and both are already in place:

- `django.contrib.admin` is in `INSTALLED_APPS` in `config/settings.py`.
- `path("admin/", admin.site.urls)` is in `config/urls.py`.

To log in, create a superuser once:

```bash
python manage.py createsuperuser
python manage.py runserver
```

Then open `http://127.0.0.1:8000/admin/`. You will see users and groups, but not your models, because you have not registered them yet.

## 2. Register a model
Registering tells the admin that a model exists. The simplest form is one line:

```python
from django.contrib import admin
from .models import Book

admin.site.register(Book)
```

Most of the time you use a `ModelAdmin` class instead, which describes how the model's pages look:

```python
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_year")
```

`@admin.register(Book)` does the same as `admin.site.register(Book, BookAdmin)`. Use the decorator; it keeps the class next to its registration.

**Register each model once.** Registering the same model twice raises `AlreadyRegistered`.

## 3. Shape the list page
These `ModelAdmin` options cover most needs:

| Option | What it does | Example |
|---|---|---|
| `list_display` | columns in the list page | `("title", "author", "published_year")` |
| `search_fields` | fields matched by the search box | `("title", "author__name")` |
| `list_filter` | sidebar filters | `("published_year",)` |
| `ordering` | default sort | `("title",)` |
| `readonly_fields` | shown but not editable | `("created_at",)` |

A foreign key in `list_display` shows the related object's `__str__`. A search field that follows a relation uses a double underscore, as `author__name` does.

## 4. Edit related rows on the same page: inlines
An **inline** shows a model's rows on its parent's page. Here, an author's page can list and edit their books without a trip to the book list:

```python
class BookInline(admin.TabularInline):  # StackedInline stacks each row vertically
    model = Book
    extra = 0  # no blank rows for adding (Django's default is 3)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    inlines = [BookInline]
```

Use `TabularInline` for short rows and `StackedInline` for rows with many fields. An inline is a class inside the parent's `ModelAdmin`, not a separate registration.

## 5. Try it
You can only run this on the library example if you add those models to a scratch project, so for the Gameya project, try it once the module's first admin TODOs are written:

1. Run `runserver`, log in at `/admin/`, and open the Member list.
2. Search for a member by part of their name.
3. Open a gameya page and check that its members appear on the same page, as an inline.

Predict before you look: what does the list page show if you never set `list_display`? (Hint: the default is `__str__`.)

## 6. Forms: check input before you trust it
Anything a user types is untrusted. A form does three jobs:
1. **Parse**: turn text from a request into Python values (`"12"` becomes `12`, `"2026-10-11"` becomes a date).
2. **Validate**: reject values that are wrong for the field (too long, too small, a week that does not exist).
3. **Report**: keep the errors, so a template can show them next to each field.

A form given data with `data=` is **bound**. Call `is_valid()` on it, then read the good values from `cleaned_data` and the errors from `errors`. Never read from the raw request data directly. A form created without `data=` is **unbound**: its `is_valid()` returns `False` and it has no errors to show.

```python
form = ContactForm(data={"name": "  Sara ", "email": "sara@example.com", "message": "Hi"})
if form.is_valid():
    form.cleaned_data["name"]  # "Sara": parsed and stripped
else:
    form.errors  # a dict: field name -> list of messages
```

## 7. A plain form: `forms.Form`
Use `forms.Form` when the data does not map to one model, for example a contact form that sends an email instead of saving a row:

```python
from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=80)  # required, stripped of spaces by default
    email = forms.EmailField()
    message = forms.CharField(max_length=500)
```

Field classes do the parsing and the common checks. `CharField` strips spaces, so `"   "` becomes an empty string and fails `required`. For a rule that no field class covers, write `clean_<fieldname>`. It runs after that field's own checks have passed, so the value is safe to use:

```python
class ContactForm(forms.Form):
    ...

    def clean_name(self):
        name = self.cleaned_data["name"]
        if any(character.isdigit() for character in name):
            raise forms.ValidationError("A name cannot contain digits.")
        return name  # always return the cleaned value
```

## 8. A form from a model: `ModelForm`
A `ModelForm` builds its fields from a model and saves to it. Set `Meta.model` and `Meta.fields`:

```python
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "published_year"]
```

Its `is_valid()` also runs the **model's** checks: the field types and `max_length`, the model's `clean()`, and the model's constraints (`UniqueConstraint` and `CheckConstraint`). A duplicate is caught here, before the database raises an `IntegrityError`. A constraint's error appears in `form.non_field_errors()` when it covers several fields. A constraint is skipped if one of its fields already failed or is not on the form.

```python
form = BookForm(data=request_data)
if form.is_valid():
    book = form.save()  # creates the Book row
```

Django's admin builds a `ModelForm` for every model it shows. So the admin runs the same checks, and shows the errors on the page instead of crashing. The admin uses a default `ModelForm` unless you set `form = YourForm` on its `ModelAdmin`.

## 9. Where validation happens, and in what order
Validation runs in these steps, and each step can add errors:

1. **Per field**: parsing and field rules (`max_length`, `min_value`, `required`), then `clean_<field>()` for that field.
2. **Form**: `clean()`, for rules that involve several fields. Set an error on one field with `self.add_error("check_out", "...")`, or on the whole form with `raise forms.ValidationError("...")`.
3. **Model** (only for a `ModelForm`): the model's `clean()`, then its constraints.

Three things to remember:

- **A field that failed is missing from `cleaned_data`.** Step 2 must use `cleaned_data.get("check_in")` and check for `None` before it uses the value.
- **Step 3 runs even when a field failed.** So a model's `clean()` must check that the values it reads are set. A model `clean()` that reads a missing value crashes with an error like `TypeError: '<=' not supported between instances of 'NoneType' and 'date'`. That crash is a bug in the model, not in the form.
- **Call `super().clean()` first in a `ModelForm`.** `ModelForm.clean()` sets up the uniqueness check. A `clean()` that skips it silently turns that check off.

Example: a booking form where check-out must be after check-in. That is a rule about two fields, so it goes in the form's `clean()`:

```python
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ["room", "check_in", "check_out"]

    def clean(self):
        cleaned = super().clean()
        check_in = cleaned.get("check_in")
        check_out = cleaned.get("check_out")
        if check_in and check_out and check_out <= check_in:
            self.add_error("check_out", "Check-out must be after check-in.")
        return cleaned
```

And the model's `clean()` for the same rule must survive a missing value, because step 3 runs even when step 1 failed:

```python
class Reservation(models.Model):
    ...

    def clean(self):
        # Guard first: the form may call this with a missing date.
        if self.check_in and self.check_out and self.check_out <= self.check_in:
            raise ValidationError("Check-out must be after check-in.")
```

## 10. Showing errors
Templates (module 05) loop over the errors. Here is the data you have to work with, for the booking form above:

```python
form.errors  # {"check_out": ["Check-out must be after check-in."]}
form.non_field_errors()  # errors that are not tied to one field
form.has_error("check_out")  # True
```

## 11. Forms in the browser need a CSRF token
A form that changes data and is posted from a template must include `{% csrf_token %}` (module 05). Without it, Django rejects the request with a 403. The admin already includes the token on its own pages, which is one reason to use it for internal screens. Module 11 covers CSRF in depth.

## 12. Habits
- Write the rule as a test first, then the code. The tests in `test_admin_forms.py` are the rules for this module.
- Put a rule where it fits best. A rule about one field goes in a field check. A rule about several fields goes in the form's `clean()`. A rule every form and the admin must share goes in the model's `clean()`.
- A model's `clean()` runs only through `full_clean()`, which forms and the admin call. `save()`, `objects.create()` and scripts skip it. For a rule that must hold no matter how a row is written, use a database constraint.
- Use `cleaned_data.get(...)` in `clean()`, never `cleaned_data[...]`.
- Never trust `request.POST` directly. Always go through a form.

## Check your understanding
1. What is the difference between `list_display` and `search_fields`?
2. What does an inline let a parent page do that a separate list page does not?
3. In what order do the field checks, `clean_<field>()`, the form's `clean()` and the model's `clean()` run?
4. Why must a model's `clean()` check for `None` before it compares dates, even though the form already checks the fields?
5. A second `Book` with the same author and title is created from the shell with `Book.objects.create(...)`. Does the model's `clean()` stop it? What does, and what error do you get?
6. When would you choose `forms.Form` over `ModelForm`?

## Do the exercises
1. Read `circles/admin.py`. Each `TODO` names a class to write. Work through them in order.
2. Read `circles/forms.py`. Write `PaymentForm` first, then `JoinForm`.
3. Run `python manage.py test circles.tests.test_admin_forms` after each `TODO`. The tests fail until the matching code is written. Stop when all of them pass.
4. Check the admin in the browser: `runserver`, then `/admin/`. Add a gameya, its members and a payment.

**Stretch (not tested):** set `form = PaymentForm` on `PaymentAdmin`. Then the admin refuses a payment below the weekly due, as the form does. Try a short payment in the browser to see the error.

**Project step:** the Gameya admin is your back office for the gameya. After this module, you can record every member and payment without the shell. Week 6 uses these forms in the public pages.

**Done when:** all of `test_admin_forms` passes, and you can explain the validation steps in section 9 without notes.
