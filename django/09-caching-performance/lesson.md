# Module 09 (Django): Caching and performance

By the end you can count the queries a page runs, remove N+1 queries with `select_related` and `prefetch_related`, keep a computed value in the cache, and clear it when the data changes.

**Before you start:** finish modules 02 to 08. This module uses the models, the query tests and the pytest suite from module 08.

**Setup:** nothing new to install. The cache framework ships with Django. Work in `django/gameya_site`, and run the module's tests with `pytest circles/tests/test_performance.py`.

**How to read the examples:** the code here uses a made-up library app with three models: `Book` (title), `Reader` (name) and `Review` (book, reader, stars, summary). It is not part of gameya_site. Learn the pattern here, then apply it to Gameya.

## 1. Measure before you change anything
Guessing where the time goes is slow. Count the queries first. `CaptureQueriesContext` records every query that runs inside its `with` block:

```python
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as context:
    for review in Review.objects.all():
        print(review.reader.name)

print(len(context.captured_queries))
print(context.captured_queries[0]["sql"])
```

**Try it:** in `python manage.py shell` in `django/gameya_site`, create a few payments, then run the same block with `Payment.objects.all()` and `payment.member.name` in place of the review and reader. Read the count. The next section explains the number you see.

## 2. The N+1 problem
The loop above runs one query for the reviews, then one more for each review's reader. With `n` reviews, that is `n + 1` queries. Each query is fast, but the total grows with the data, and a page that works for ten rows can time out at a thousand. This is the N+1 problem.

The fix is to load the related rows in the same query, or in one more query for all of them.

## 3. `select_related`: the "one" side of a relation
For a foreign key (or a one-to-one), `select_related` joins the related table in the same query:

```python
for review in Review.objects.select_related("reader"):
    print(review.reader.name)
```

**Try it:** run the Gameya version of the block from section 1 again, with `select_related("member")` added to `Payment.objects.all()`. The count drops to one.

## 4. `prefetch_related`: the "many" side of a relation
For a reverse foreign key, such as the reviews of a book, or a many-to-many relation, a join would repeat the book's columns on every row. `prefetch_related` runs one extra query for the related rows, then attaches them to the books in Python:

```python
books = Book.objects.prefetch_related("review_set")  # 2 queries, however many books
for book in books:
    print(book.title, [review.stars for review in book.review_set.all()])
```

Use `.all()` after a prefetch. Calling `.filter()` on it runs a new query, because the prefetched list is ignored:

```python
book.review_set.filter(stars=5)  # a new query for every book: the prefetch is not used
```

To prefetch a filtered list, use `Prefetch`, and give the result its own name:

```python
from django.db.models import Prefetch

books = Book.objects.prefetch_related(
    Prefetch("review_set", queryset=Review.objects.filter(stars=5), to_attr="five_star_reviews")
)
for book in books:
    print(book.title, len(book.five_star_reviews))
```

## 5. `only` and `defer`: load fewer columns
`only("title")` loads just the named columns, and `defer("summary")` skips some. This helps when rows are large. Be careful: if the loop later reads a deferred field, Django runs one query for each row. That is the N+1 problem again, so use `only` and `defer` only for fields the code truly never reads.

## 6. Let the database do the sums
Totals, counts and averages belong in the database, with `annotate` and `aggregate` from module 02. Looping in Python over rows that are already loaded is fine for small lists, but the database is faster for large ones. Both work. Count the queries and decide.

## 7. The cache framework
A cache keeps the result of slow work so that the next request can reuse it. Django's cache has one setting, `CACHES`:

```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "library",
        "TIMEOUT": 60,  # seconds; the TODO in your project says which value to use
    }
}
```

`LocMemCache` keeps entries in the memory of one process. Each worker process has its own cache, and a restart empties it. Week 9 switches to Redis, which every process shares.

The API is short:

```python
from django.core.cache import cache

cache.set("book:1:summary", {"reviews": 3}, timeout=60)
cache.get("book:1:summary")  # the value, or None when it is missing or expired
cache.get("book:1:summary", default={})  # or your own default
cache.delete("book:1:summary")
```

**Try it:** in the shell, set a key, read it, delete it, and read it again. Check that the last read gives `None`.

Three rules keep the cache safe:
- Name keys after what they hold and the id they belong to, such as `book:1:summary`. A key is shared by everyone who uses the cache, so it must be unique.
- Store only values that can be pickled (plain data, such as dicts, lists, numbers and strings).
- Code must still work when an entry is missing. A cache makes things faster. It is never the only copy of the data.

## 8. Invalidation: clear the cache when the data changes
A cached value goes stale when its data changes. The usual fix is to delete the entry when the data is written. Module 07 gave you signals, so a receiver can do it:

```python
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


@receiver(post_save, sender=Review)
@receiver(post_delete, sender=Review)
def clear_book_summary(sender, instance, **kwargs):
    cache.delete(f"book:{instance.book_id}:summary")
```

Remember the module 07 rule: receivers run only when the app loads them, so `ready()` must import the module.

Three gotchas:
- `QuerySet.update()`, `bulk_create()` and `bulk_update()` do not send signals. After them, delete the cache entries yourself.
- Deleting a parent sends `post_delete` for each child, so cascades clear the cache too.
- A request can read the old data again between your write and the commit, and cache it again. Clear on commit instead: `transaction.on_commit(lambda: cache.delete(key))`. Django runs that callback only after the transaction commits, so no reader can rebuild the entry from uncommitted data.

Test invalidation directly: read the value, change the data, read again, and check the new value. Cached tests also need an empty cache at the start of each test, because the cache outlives the transaction rollback that resets the database.

## 9. Caching a whole page (read only)
Django can cache a view's full response: `@cache_page(60)` keeps a GET response for 60 seconds, keyed by the URL. A logged-in page needs `vary_on_cookie`, or one user's page would be served to another. A template can cache a fragment:

```django
{% load cache %}
{% cache 300 book_list book.pk %}
  ...expensive part...
{% endcache %}
```

Page caches are simple, but they go stale: `cache_page` does not know when the data changed. Use them for pages that can be a little old.

## 10. Measure, then decide
- Optimise the query that runs most often, or the one that is slowest. Fewer queries is not always faster: a prefetch of a million rows can cost more than ten small queries.
- Cache what is expensive to build and read often. Do not cache what changes on every request.
- Put the query count in a test, so a later change cannot bring the N+1 back.

## Check your understanding
1. Why does `select_related` use a join, while `prefetch_related` runs a second query?
2. A loop uses `book.review_set.filter(stars=5)` after a prefetch. How many queries run, and why?
3. What does `only("title")` cost if the loop later reads `book.summary`?
4. Why does a `QuerySet.update()` leave a cached value stale, when a `save()` would not?
5. Why must a test empty the cache before it starts?
6. Why is it safer to clear a cache entry on commit than at the moment of the write?
7. The cache loses all its entries. What still works, and what gets slower?

## Do the exercises
1. **Measure.** After TODO 31, open `python manage.py shell` and use `CaptureQueriesContext` to count the queries that `build_summary` runs for a gameya you create. Then add a second member and count again.
2. **Settings.** Add the `CACHES` setting (TODO 34), with the timeout that the TODO asks for.
3. **Summary.** Write `build_summary` (TODO 31) so that the number of queries does not grow with the members. Use prefetching.
4. **Cache.** Write `gameya_summary` (TODO 32), which uses the cache and rebuilds on a miss.
5. **Invalidation.** Write `invalidate_summary` (TODO 33), and the receivers in `circles/signals.py`, so that a member or a payment change clears the entry.
6. **Run the file.** Run `pytest circles/tests/test_performance.py`. Stop when all 14 tests pass.
7. **Try a failure on purpose.** Remove the prefetch from `build_summary`, run the tests, and read the query-count failure. Then put it back.
8. **Run everything.** Run `pytest` in `django/gameya_site`. Earlier tests must still pass, because the cache must not change what the pages show.

**Stretch (not tested):** put `@cache_page(60)` on the gameya list view from module 04. Write a test that a second request runs no queries. Then add a payment, and explain why the list can show the old data until the cache expires.

**Project step:** the gameya summary is now built with a fixed number of queries and cached, and it clears on every change. Later modules can reuse `gameya_summary` without repeating the work.

## Exit checklist
- [ ] `pytest circles/tests/test_performance.py` passes all 14 tests.
- [ ] You can count the queries of a block with `CaptureQueriesContext`, and explain where an N+1 comes from.
- [ ] You can say when to use `select_related` and when to use `prefetch_related`.
- [ ] You can name the three rules for cache keys and values, and say what invalidation must cover.
