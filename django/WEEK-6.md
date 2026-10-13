# Week 6: Admin, forms, views and templates

Goal by Saturday: run the Gameya back office in the admin, accept input only through forms that validate it, and serve the same data as a JSON API and as HTML pages. Everything this week sits on the week 5 models, so finish `test_models` first if anything is still red.

Daily shape: **Learn 1–1.5 h → Build 1–1.5 h → Drill 20 min → Wrap-up 10 min** (see [the plan](../docs/12-week-plan.md)). On a short day (2 h), do Learn and Wrap-up only. The drills for this week are in [drills.md](../docs/drills.md#week-6).

Run the commands below from `django/gameya_site`, with the virtual environment from week 5 active.

| Day | Learn | Build / exercises | Drill |
|---|---|---|---|
| **1** | [03 Admin and forms](03-admin-forms/lesson.md) sections 1–5: registering models, the list page, inlines | `circles/admin.py`, one `TODO` at a time; `python manage.py createsuperuser`, then add a gameya, members and a payment at `/admin/` | 1 easy problem |
| **2** | 03 sections 6–12: `Form`, `ModelForm`, the order validation runs in, errors, CSRF | `PaymentForm`, then `JoinForm` in `circles/forms.py`; all of `circles.tests.test_admin_forms` passes | 1 easy problem |
| **3** | [04 Views](04-views/lesson.md) sections 1–5: function vs class views, dispatch, responses, reading input | TODO 5 (`GameyaList`) and TODO 8 (its route): `GameyaListTests` passes | 1 problem |
| **4** | 04 sections 6–12: `DetailView`, `get_object_or_404`, posted data, N+1 | TODOs 6 and 9, then 7 and 10; all of `circles.tests.test_class_views` passes; try each URL with `curl.exe -i` | 1 problem |
| **5** | [05 Templates](05-templates/lesson.md) sections 1–8: variables, filters, tags, autoescaping, inheritance, static files | `base.html`, `about.html` extends it, `circles/static/circles/site.css` | 1 problem |
| **6** | 05 sections 9–12: class-based views with templates, forms in templates, where logic belongs | TODOs 11 to 14, `home.html` and `gameya_detail.html`; all 20 tests in `circles.tests.test_templates` pass | 1 problem |
| **Review day** | Redo the weakest TODO from memory in a scratch copy | Run the whole suite: `python manage.py test`; commit; open `/` and a gameya page in the browser | Write 2–3 interview questions with your own answers, from [the question bank](../docs/interview-questions.md) |

## Stretch goals
- Set `form = PaymentForm` on `PaymentAdmin`, so the admin refuses a short payment the same way the form does (module 03).
- Add a `DELETE` route for one payment that answers 204, and test it with the test client (module 04).
- Add `Member.is_active()` and show "Inactive" in the members table when `shares` is 0 (module 05).

## Daily wrap-up
```
Date:
Learned:
Confused by:
Tomorrow:
```

## Checkpoint (end of week)
Without notes you can:
- [ ] Register a model in the admin with list columns, filters, search and an inline
- [ ] Say the order in which Django runs field checks, `clean_<field>()` and `clean()`, and where each error shows
- [ ] Explain why a form needs a CSRF token
- [ ] Choose between a function view and a class-based view for a given job, and say why
- [ ] Pick the right status code for a missing object, a bad form and a created row
- [ ] Build a page from a base template with `{% extends %}` and `{% block %}`
- [ ] Explain what autoescaping protects against, and where it does not apply
- [ ] Say why a calculation belongs in a model method, not in the template

## Notes for Week 7
Next week puts a REST API in front of the same models with Django REST Framework, then wraps every request in middleware. Keep your views: module 06 builds the API next to them, so you can compare the two.
