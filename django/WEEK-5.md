# Week 5: Django architecture, models and the ORM

Goal by Saturday: explain how a Django request becomes a response, and model the Gameya as four related tables that you can query efficiently. You start the Django version of Gameya, the project you will carry through weeks 5–9.

Daily shape: **Learn 1–1.5 h → Build 1–1.5 h → Drill 20 min → Wrap-up 10 min** (see [the plan](../docs/12-week-plan.md)). On a short day (2 h), do Learn and Wrap-up only.

## Setup (Day 1, 15 minutes)
```bash
cd django/gameya_site
python -m venv .venv
.venv\Scripts\Activate.ps1            # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py check                # should say: no issues
python manage.py test                 # many tests fail on purpose: they are your to-do list
```
The tests are the specification. A new test passing is your progress bar.

| Day | Learn | Build / exercises | Drill |
|---|---|---|---|
| **1** | [01 Architecture](01-architecture/lesson.md) sections 1–7: MTV, the request cycle, project vs app, settings | Setup above; generate a throwaway project once to see the files; read `config/settings.py` | 1 easy problem |
| **2** | 01 sections 8–12: URL routing, views, templates | `circles.tests.test_architecture`: views, URLs and `about.html` until all pass; open `runserver` and visit each page | 1 easy problem |
| **3** | [02 Models and the ORM](02-models-orm/lesson.md) sections 1–5: fields, relationships, Meta, constraints, migrations | `Gameya` and `Member` in `models.py`, `makemigrations`, `migrate`, read the migration | 1 problem |
| **4** | 02 sections 6–7: creating rows, QuerySets, lookups | `Payment` and `PayoutSlot`, `status()`, `is_advance`; all of `circles.tests.test_models` passes | 1 problem |
| **5** | 02 sections 8–11: aggregation, annotation, N+1, transactions | `queries.py` functions 1–4 (`unpaid_members`, `total_collected`, `member_totals`, `weekly_summary`) | 1 problem |
| **6** | Review | `queries.py` functions 5–7, then explore in `manage.py shell`; print `qs.query` for each | 1 problem |
| **Review day** | Redo your weakest query from memory | Run the whole suite: `python manage.py test`; commit; stretch goals below | Write 2–3 interview questions with your own answers |

## Stretch goals
- Move the query functions onto a custom `QuerySet` and manager (`Member.objects.with_totals()`).
- Add a `Member.balance_due(today)` that returns how much the member owes for all started, unpaid weeks.
- Seed the database with a management command that creates a demo gameya, so `runserver` shows data next week.
- Compare the SQL of `exclude(payments__week=1)` with a hand-written one using `print(qs.query)`.

## Daily wrap-up
```
Date:
Learned:
Confused by:
Tomorrow:
```

## Checkpoint (end of week)
Without notes you can:
- [ ] Trace a request from the browser to the response, naming each Django layer
- [ ] Explain project vs app, and what `INSTALLED_APPS`, `DEBUG` and `SECRET_KEY` do
- [ ] Route a URL with a typed converter to a view, and reverse it by name
- [ ] Define models with `ForeignKey`, `related_name`, `on_delete`, constraints and `Meta`
- [ ] Generate, read and apply a migration, and say why you commit migrations
- [ ] Write filters across relationships, `Q`, `F`, `annotate`, `aggregate` and a `GROUP BY` with `values().annotate()`
- [ ] Explain the N+1 problem and fix it with `select_related`
- [ ] Say why `turns` and `payout` are properties, not columns

## Notes for Week 6
Next week adds the admin site, forms, class-based views and templates on these same models, so keep your `circles/` code. If a model test still fails, finish it before moving on.
