# Module 03 (Django): Admin and forms

By the end you can register models in the Django admin and shape their pages, and you can write forms that check user input before it reaches your database: from a model with `ModelForm`, and from scratch with `forms.Form`.

**Before you start:** finish module 02. The admin and forms are built on the `Gameya`, `Member`, `Payment` and `PayoutSlot` models.

## 1. The admin is a back office you get for free
Django's admin is a web interface generated from your models. It gives you lists, search, filters, and add and edit pages, with no templates to write. Two pieces make it work:

- `django.contrib.admin` is in `INSTALLED_APPS` (it already is in `config/settings.py`).
- `config/urls.py` has `path("admin/", admin.site.urls)` (it already does).

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
from .models import Gameya

admin.site.register(Gameya)
```

Most of the time you use a `ModelAdmin` class instead, which describes how the model's pages look:

```python
@admin.register(Gameya)
class GameyaAdmin(admin.ModelAdmin):
    list_display = ("name", "weeks", "share_value")
```

`@admin.register(Model)` does the same as `admin.site.register(Model, GameyaAdmin)`. Use whichever reads better; the decorator keeps the class next to the registration.

## 3. Shape the list page
These `ModelAdmin` options cover most needs:

| Option | What it does | Example |
|---|---|---|
| `list_display` | columns in the list page | `("name", "gameya", "shares")` |
| `search_fields` | fields matched by the search box | `("name",)` |
| `list_filter` | sidebar filters | `("gameya",)` |
| `ordering` | default sort | `("name",)` |
| `readonly_fields` | shown but not editable | `("created_at",)` |

A foreign key in `list_display` shows the related object's `__str__`. Search fields that follow a relation use the double underscore, for example `"gameya__name"`.

## 4. Edit related rows on the same page: inlines
An **inline** shows a model's rows on its parent's page. The gameya page can list and edit its members without a trip to the member list:

```python
class MemberInline(admin.TabularInline):   # StackedInline stacks each row vertically
    model = Member
    extra = 0                               # no empty rows by default

@admin.register(Gameya)
class GameyaAdmin(admin.ModelAdmin):
    inlines = [MemberInline]
```

`extra` is how many blank rows to show for adding. Use `TabularInline` for short rows and `StackedInline` for rows with many fields.

## 5. Try it
1. Register `Member` with a `MemberAdmin` that has `list_display`, `search_fields` and `list_filter`.
2. Run `runserver`, open `/admin/`, and add a gameya and two members. Search for one of them by name.
3. Open the gameya page and confirm the members appear inline.

Predict before you look: what would the list page show if `list_display` were empty? (Hint: `__str__`.)

## 6. Forms: check input before you trust it
Anything a user types is untrusted. A form does three jobs:
1. **Parse**: turn text from a request into Python values (`"12"` becomes `12`, `"2026-10-11"` becomes a date).
2. **Validate**: reject values that are wrong for the field (too long, too small, a week that does not exist).
3. **Report**: keep the errors, so a template can show them next to each field.

Check the result with `is_valid()`. Read the good values from `cleaned_data` and the errors from `errors`. Never read from `data` directly.

```python
form = SomeForm(data={"name": "  Sara ", "shares": "2"})
if form.is_valid():
    form.cleaned_data["name"]     # "Sara": parsed and stripped
else:
    form.errors                   # a dict: field name -> list of messages
```

## 7. A plain form: `forms.Form`
Use `forms.Form` when the data does not map to one model, for example a sign-up form that creates a member in a different way:

```python
from django import forms

class JoinForm(forms.Form):
    name = forms.CharField(max_length=80)       # required, stripped of spaces by default
    shares = forms.IntegerField(min_value=1, max_value=5)
```

Field classes do the parsing and the common checks. `CharField` strips spaces, so `"   "` becomes an empty string and fails `required`. For a rule that no field class covers, write `clean_<fieldname>`:

```python
class JoinForm(forms.Form):
    ...
    def clean_name(self):
        name = self.cleaned_data["name"]
        if name.lower() == "admin":
            raise forms.ValidationError("That name is reserved.")
        return name                              # always return the cleaned value
```

## 8. A form from a model: `ModelForm`
A `ModelForm` builds its fields from a model and saves to it. Set `Meta.model` and `Meta.fields`:

```python
class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["member", "week", "paid_on", "amount"]
```

Its `is_valid()` also runs the **model's** checks: the field types and `max_length`, the model's `clean()`, and every `UniqueConstraint` and `CheckConstraint`. A duplicate `(member, week)` is caught here, before the database raises an `IntegrityError`. Multi-field constraint errors appear in `form.non_field_errors()`.

```python
form = PaymentForm(data=request_data)
if form.is_valid():
    payment = form.save()        # creates the Payment row
```

## 9. Where validation happens, and in what order
Validation runs in this order, and each step can add errors:

1. **Per field**: parsing and field rules (`max_length`, `min_value`, `required`), then `clean_<field>()` for that field.
2. **Form**: `clean()`, for rules that involve several fields. Set errors on one field with `self.add_error("amount", "...")`, or on the whole form with `raise ValidationError("...")`.
3. **Model** (only for a `ModelForm`): the model's `clean()` and its constraints.

Two things to remember:
- If a field failed in step 1, it is missing from `cleaned_data`. Step 2 must use `cleaned_data.get("member")` and check for `None` before it uses the value. This is why a missing member must not crash the form.
- Return `cleaned_data` from `clean()`.

Example: a payment must cover at least one week's due amount. That rule needs the member and the amount, so it belongs in `clean()`:

```python
def clean(self):
    cleaned = super().clean()
    member = cleaned.get("member")
    amount = cleaned.get("amount")
    if member and amount is not None and amount < member.due():
        self.add_error("amount", f"Must be at least {member.due()} for one week.")
    return cleaned
```

## 10. Showing errors
Templates (module 05) loop over the errors. Here is the data you have to work with:

```python
form.errors                  # {"amount": ["Must be at least 1000 for one week."]}
form.non_field_errors()      # errors that are not tied to one field
form.has_error("amount")     # True
```

## 11. Forms in the browser need a CSRF token
A form that changes data and is posted from a template must include `{% csrf_token %}` (module 05). Without it, Django rejects the request with a 403. The admin already includes the token on its own pages, which is one reason to use it for internal screens. Module 11 covers CSRF in depth.

## 12. Habits
- Write the rule first as a test, then the form. The tests in `test_admin_forms.py` are the rules for this module.
- Put a rule in the narrowest place that can enforce it: a field rule for one field, `clean()` for several, the model for anything that must hold no matter who writes the row.
- Use `cleaned_data.get(...)` in `clean()`, never `cleaned_data[...]`.
- Never trust `request.POST` directly. Always go through a form.

## Check your understanding
1. What is the difference between `list_display` and `search_fields`?
2. Why does `TabularInline` on the gameya page save you a click for each member?
3. In what order do `clean_<field>()`, `clean()` and the model's `clean()` run?
4. Why must `clean()` use `cleaned_data.get("member")` and not `cleaned_data["member"]`?
5. A payment for week 3 already exists for this member. Which layer rejects the second one, and what kind of error does the form show?
6. When would you choose `forms.Form` over `ModelForm`?

## Do the exercises
1. Read `circles/admin.py`. Each `TODO` names a class to write. Work through them in order.
2. Read `circles/forms.py`. Write `PaymentForm` first, then `JoinForm`.
3. Run `python manage.py test circles.tests.test_admin_forms` after each `TODO`. The tests fail until the matching code is written. Stop when all of them pass.
4. Check the admin in the browser: `runserver`, then `/admin/`. Add a gameya, its members and a payment.

**Project step:** the Gameya admin is your back office for the gameya. After this module, you can record every member and payment without the shell. Week 6 uses these forms in the public pages.

**Done when:** all of `test_admin_forms` passes, and you can explain the three validation layers in section 9 without notes.
