# Module 02 (Django): Models and the ORM

By the end you can design tables as Python classes, evolve them with migrations, and query them efficiently with the ORM, including relationships, aggregation and N+1 avoidance.

## 1. What the ORM is
An **ORM** (object-relational mapper) lets you work with database tables as Python classes and rows as objects. One class = one table, one attribute = one column, one instance = one row. Django generates the SQL for you and keeps your schema history in **migrations**.

```python
class Gameya(models.Model):
    name = models.CharField(max_length=80)
    weeks = models.PositiveSmallIntegerField()
```
Django adds an automatic `id` primary key.

## 2. Fields
Choose the field type that matches the data; Django validates and the database stores accordingly.

| Field | Use | Notes |
|---|---|---|
| `CharField(max_length=80)` | short text | `max_length` required |
| `TextField()` | long text | |
| `IntegerField`, `PositiveIntegerField`, `PositiveSmallIntegerField` | whole numbers | Positive* allow 0 and up |
| `DecimalField(max_digits, decimal_places)` | money | never use `FloatField` for money |
| `BooleanField(default=False)` | yes/no | |
| `DateField`, `DateTimeField` | dates | `auto_now_add=True` sets it on creation |
| `ForeignKey`, `OneToOneField`, `ManyToManyField` | relationships | next section |

Common options: `null=True` (database allows NULL), `blank=True` (forms may leave it empty), `default=...`, `unique=True`, `choices=...`, `db_index=True`, `validators=[...]`. For text, prefer `blank=True` with `default=""` over `null=True`.

## 3. Relationships
```python
class Member(models.Model):
    gameya = models.ForeignKey(Gameya, on_delete=models.CASCADE, related_name="members")
    name = models.CharField(max_length=80)
```
- **`ForeignKey`** (many-to-one): many members belong to one gameya. The column is `gameya_id`.
- **`on_delete`** decides what happens when the parent is deleted: `CASCADE` (delete the children too), `SET_NULL` (needs `null=True`), `PROTECT` (refuse), `SET_DEFAULT`.
- **`related_name`** names the reverse accessor: `gameya.members.all()`. Without it, Django uses `member_set`.
- **`OneToOneField`**: exactly one related row (a profile for a user).
- **`ManyToManyField`**: many on both sides (tags on articles). Django creates the join table.

## 4. Meta, constraints and methods
```python
class Gameya(models.Model):
    ...

    class Meta:
        ordering = ["name"]  # default ordering
        constraints = [
            models.CheckConstraint(condition=Q(weeks__gte=1), name="gameya_weeks_positive"),
            models.UniqueConstraint(fields=["gameya", "name"], name="..."),
        ]

    def __str__(self):  # shown in the admin and the shell
        return self.name

    @property
    def turns(self):  # computed, not stored
        return self.weeks * self.per_week
```
- **Put rules in the database** with constraints, not only in Python. Code can be bypassed (a script, another service); a constraint cannot.
- **Derive, don't store:** a value you can compute from other columns (turns, payout) should be a property, so it can never drift out of sync.
- Validation in Python: override `clean()` and call `full_clean()` (forms and the admin do it for you). `save()` does **not** call `full_clean()`.

## 5. Migrations
Migrations are version control for your schema.
```bash
python manage.py makemigrations          # compare models with migrations, write a new migration file
python manage.py migrate                 # apply migrations to the database
python manage.py showmigrations          # what is applied
python manage.py sqlmigrate circles 0001 # see the SQL a migration runs
```
Rules:
- Run `makemigrations` after **every** model change, then read the generated file.
- **Commit migrations** with the model change. They are part of the code.
- Never edit an applied migration; add a new one.
- Renaming or removing fields needs care on real data (add, copy, then remove).
- `python manage.py makemigrations --check` fails when models and migrations disagree. Our tests use it.

## 6. Creating and changing rows
```python
g = Gameya.objects.create(name="Alf", start_date=date(2026, 10, 10), weeks=10, share_value=100)
m = Member(gameya=g, name="Ali")
m.save()  # INSERT
m.shares = 2
m.save()  # UPDATE
m.delete()  # DELETE
Member.objects.filter(shares=1).update(shares=2)  # one UPDATE for many rows
Member.objects.bulk_create([Member(...), Member(...)])  # one INSERT for many rows
obj, created = Member.objects.get_or_create(gameya=g, name="Sara")
```

## 7. QuerySets
`Model.objects` is the **manager**; `.all()`, `.filter()` and friends return a **QuerySet**: a lazy description of a query.
```python
qs = Member.objects.filter(gameya=g).exclude(shares=1).order_by("name")  # no SQL yet
list(qs)  # now it runs (also: iterating, len(), bool(), slicing with a step)
qs[:10]  # LIMIT 10 (still lazy)
qs.first(), qs.last(), qs.count(), qs.exists()
Member.objects.get(id=1)  # exactly one row; raises DoesNotExist / MultipleObjectsReturned
```
Key ideas:
- **Lazy:** building a QuerySet costs nothing; the query runs when you read results. Chaining adds conditions.
- **Cached:** once evaluated, the same QuerySet object reuses its results.
- Use `.exists()` instead of `len(qs) > 0`, and `.count()` instead of `len(list(qs))`.

### Lookups
Double underscores add operators and follow relationships:
```python
Member.objects.filter(
    name__startswith="A"
)  # also __contains, __icontains, __in, __gte, __lt, __isnull
Member.objects.filter(name__in=["Ali", "Sara"])
Payment.objects.filter(paid_on__gte=date(2026, 10, 1))
Payment.objects.filter(member__gameya=g)  # across a ForeignKey
Member.objects.filter(payments__week=1)  # across the reverse relation
Member.objects.exclude(payments__week=1)  # members with no payment for week 1
```

### `Q` and `F`
```python
from django.db.models import Q, F

Member.objects.filter(Q(shares__gt=1) | Q(name="Ali"))  # OR; & is AND; ~Q is NOT
Payment.objects.filter(amount__lt=F("member__shares") * 50)  # compare two columns, in the database
Member.objects.update(shares=F("shares") + 1)  # increment without a race condition
```

### Values
```python
Member.objects.values("name", "shares")  # dicts instead of objects
Member.objects.values_list("name", flat=True)  # a flat list of names
```

## 8. Aggregation and annotation
Do arithmetic in the database, not in Python loops.
```python
from django.db.models import Count, Sum, Avg, Min, Max
from django.db.models.functions import Coalesce

Payment.objects.aggregate(total=Sum("amount"))  # {"total": 500}  (None if empty)
Payment.objects.aggregate(total=Coalesce(Sum("amount"), 0))  # 0 when empty

Member.objects.annotate(paid=Coalesce(Sum("payments__amount"), 0), n=Count("payments"))
# every member now has .paid and .n; one query with a JOIN and GROUP BY

Payment.objects.values("week").annotate(count=Count("id"), amount=Sum("amount")).order_by("week")
# GROUP BY week
```
- `aggregate` collapses the whole QuerySet to one dict. `annotate` adds a computed column to **every row**.
- `.values("week").annotate(...)` is how you write `GROUP BY`.
- Filtering on an annotation (`.filter(n__gt=0)`) becomes `HAVING`.

## 9. The N+1 problem
```python
for payment in Payment.objects.all():
    print(payment.member.name)  # 1 query for payments + 1 query PER payment: slow
```
Fix it by loading related rows up front:
```python
Payment.objects.select_related("member")  # SQL JOIN, for ForeignKey / OneToOne (the "one" side)
Payment.objects.select_related("member__gameya")  # follow several hops
Gameya.objects.prefetch_related("members")  # a second query, for reverse FK / ManyToMany
```
Count queries in tests with `assertNumQueries(n)`, as this module's tests do. In development, `django-debug-toolbar` shows them. Remember that a `@property` that reads `self.member.gameya` triggers a query unless it is preloaded.

## 10. Custom QuerySets and managers
Put repeated filters on the model so every caller shares them:
```python
class MemberQuerySet(models.QuerySet):
    def with_totals(self):
        return self.annotate(paid_total=Coalesce(Sum("payments__amount"), 0))


class Member(models.Model):
    ...
    objects = MemberQuerySet.as_manager()


Member.objects.filter(gameya=g).with_totals()
```
This module's `queries.py` uses plain functions; moving them onto a QuerySet is a good stretch goal.

## 11. Transactions
```python
from django.db import transaction

with transaction.atomic():
    payment.save()
    slot.save()  # both are saved, or neither is
```
Wrap multi-step writes in `atomic()`. Django tests run each test inside a transaction and roll it back, so tests stay isolated.

## 12. Working in the shell and reading SQL
```python
python manage.py shell
>>> qs = Member.objects.filter(shares__gt=1)
>>> print(qs.query)                  # the SQL Django will run
>>> from django.db import connection
>>> len(connection.queries)          # queries so far (when DEBUG is on)
```

## 13. Habits
- Design the tables first: relationships, constraints, what is stored vs derived.
- One migration per logical change; read it before applying.
- Do filtering, ordering and arithmetic in the database.
- Always ask "how many queries is this?" for anything in a loop.
- Test models with the real database (Django's `TestCase`), not mocks.

## Check your understanding
1. What is a QuerySet, and why is it lazy?
2. What do `on_delete=CASCADE` and `SET_NULL` do? When would you choose `PROTECT`?
3. Why put a rule in a `CheckConstraint` and not only in Python?
4. Why should you commit migrations, and never edit an applied one?
5. What is the difference between `aggregate` and `annotate`? Show `GROUP BY` with `values().annotate()`.
6. What is the N+1 problem, and how do `select_related` and `prefetch_related` fix it?
7. Why store `weeks` and `per_week`, but compute `turns` and `payout`?

## Do the exercises
1. Read `circles/models.py` and `circles/queries.py` (the docstrings are the specification) and the tests in `circles/tests/test_models.py` and `circles/tests/test_queries.py`.
2. Build the four models, one at a time: write the class, then `python manage.py makemigrations`, `python manage.py migrate`, then `python manage.py test circles.tests.test_models`. Read each generated migration.
3. When all of `test_models` passes, implement the seven functions in `queries.py` and run `python manage.py test circles.tests.test_queries`. Several tests count queries on purpose.
4. Open `python manage.py shell`, create a gameya, and try your queries. Print `qs.query` to see the SQL.
5. Run the whole suite: `python manage.py test`.
