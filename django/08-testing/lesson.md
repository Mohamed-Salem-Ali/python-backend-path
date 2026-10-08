# Module 08 (Django): Testing with pytest, pytest-django and factories

By the end you can write tests as plain functions, run one test with many cases, share setup through fixtures, build test data with factories, test pages and the API with the client, and check how many queries a page runs.

**Before you start:** finish modules 02 to 07. The tests use the models, the pages, the admin and the API from those modules.

**Setup (15 minutes):**
```bash
pip install -r requirements.txt
```
`requirements.txt` already lists pytest, pytest-django and factory-boy. Then write `pytest.ini` in `django/gameya_site` (TODO 28). Run tests from that folder with `pytest`. Until `pytest.ini` names the settings module, pytest stops with `ImproperlyConfigured` before any test runs. That is expected, and TODO 28 fixes it.

**How to read the examples:** the code here uses a made-up library app with three models: `Book` (title, published_on), `Reader` (name) and `Review` (book, reader, stars, summary). It is not part of gameya_site. Learn the pattern here, then apply it to Gameya in `circles/tests/`.

## 1. Two runners, one project
Module 02 onward used Django's own runner: `python manage.py test`, with `TestCase` classes and `assertEqual`. pytest is a different runner. It finds plain functions that start with `test_`, runs them, and rewrites `assert` so a failure shows the values:

```python
def test_a_book_has_a_title():
    book = Book(title="Dune")
    assert book.title == "Dune"
```

That test passes. If the title were `Dune!`, pytest would show both values and where they differ:

```text
E       AssertionError: assert 'Dune!' == 'Dune'
E         - Dune
E         + Dune!
E         ?     +
```

pytest-django connects the two. It sets up Django, gives you database and client fixtures, and runs each test in a transaction that is rolled back afterwards. Both runners work on this project. Use pytest for the new tests, and keep the old `TestCase` tests as they are.

**Try it:** after TODO 28, add a file `circles/tests/test_scratch.py` with one function that asserts `1 + 1 == 3`. Run `pytest circles/tests/test_scratch.py`, read the failure, then delete the file.

## 2. Configure pytest once: `pytest.ini`
pytest reads a `pytest.ini` file in the folder you run it from. The important line names your settings module, the dotted name that `manage.py` passes to `os.environ.setdefault`:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = yourproject.settings
python_files = test_*.py
```

Replace `yourproject.settings` with the name from your `manage.py`. `python_files` tells pytest which files are test files. Its default is already `test_*.py`, so the line is optional.

Without `DJANGO_SETTINGS_MODULE`, pytest-django cannot start Django. A test that uses the database then fails with an error, and a conftest file that imports a Django model stops the whole run before any test starts.

## 3. Parametrize: one test, many cases
When the same check applies to several inputs, write it once and list the cases. Each case is reported on its own:

```python
import pytest


@pytest.mark.parametrize(
    "days, fine",
    [(0, 0), (3, 30), (10, 100)],
    ids=["on time", "three days late", "ten days late"],
)
def test_the_late_fine_is_ten_per_day(days, fine):
    assert late_fine(days=days) == fine  # late_fine is a function you would write
```

`ids` names each case in the output, so a failing case says which one it was. Use parametrize for a table of inputs and their results, not for a single case.

## 4. Fixtures: setup shared by many tests
A fixture is a function that builds something a test needs. A test asks for it by naming it in its arguments:

```python
import pytest


@pytest.fixture
def dune(db):
    return Book.objects.create(title="Dune", published_on=date(1965, 8, 1))


def test_the_book_has_a_title(dune):
    assert dune.title == "Dune"
```

A fixture can ask for other fixtures, and pytest builds them in order. Put fixtures that many test files share in `conftest.py`, in the same folder or above. pytest finds them there without an import.

Two rules for database fixtures:
- A fixture that writes to the database must take the built-in `db` fixture. Without it, pytest-django raises an error, so the database cannot be changed by accident.
- A test that needs no database should not ask for `db`. It runs faster, and it shows that the code under test does not depend on the database.

When a fixture needs a value that depends on the test, use `request.getfixturevalue`:

```python
@pytest.mark.parametrize("who, status", [("anonymous", 401), ("reader", 403)])
def test_who_may_add_a_book(who, status, api_client, request):
    if who != "anonymous":
        token = request.getfixturevalue(f"{who}_token")
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = api_client.post("/library/books/", {"title": "Dune"})
    assert response.status_code == status
```

## 5. pytest-django's own fixtures
pytest-django gives you fixtures that match what you already know:

| Fixture | What it is |
|---|---|
| `db` | lets the test use the database; the changes are rolled back afterwards |
| `client` | a test client, like `self.client` in a `TestCase` |
| `admin_client` | a client already logged in as a superuser |
| `settings` | the settings object, where you can change a value for one test |
| `django_user_model` | the user model, for creating users in a fixture |
| `django_assert_num_queries(n)` | fails unless the block runs exactly `n` queries |
| `django_assert_max_num_queries(n)` | fails if the block runs more than `n` queries |

Code that runs on commit, such as a callback passed to `transaction.on_commit`, is not run inside a test, because the test's transaction is rolled back. To check it, use the `django_capture_on_commit_callbacks` fixture, which runs the callbacks for you. Use `@pytest.mark.django_db(transaction=True)` only when the test really needs a commit to happen, because such tests are slower.

## 6. Factories: build test data with one call
Creating objects by hand in every test repeats the same lines. A factory describes how to build a valid object, with defaults you can override:

```python
import factory


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Sequence(lambda n: f"Book {n}")
    published_on = date(1965, 8, 1)


class ReaderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Reader

    name = factory.Sequence(lambda n: f"Reader {n}")


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review

    book = factory.SubFactory(BookFactory)  # builds a book unless one is given
    reader = factory.SubFactory(ReaderFactory)
    stars = 4
    summary = factory.LazyAttribute(lambda o: f"Rated {o.stars} out of 5")
```

- `factory.Sequence` gives each object a new value: `Book 0`, `Book 1`, and so on. The counter does not reset between tests, so never write a test that depends on a particular number.
- `factory.SubFactory` builds a related object. A test can pass its own, or reach inside with a double underscore: `ReviewFactory(book__title="Dune")`.
- `factory.LazyAttribute` computes a value from the other fields of the object being built.

Use `BookFactory()` to save one object, and `BookFactory.build()` to make one without saving it. `BookFactory.create_batch(3)` saves three.

**Try it:** once TODO 29 is done, run `python manage.py shell` in `django/gameya_site`. Then run `from circles.tests.factories import GameyaFactory`, and `GameyaFactory.build().pk`. It prints `None`, because `build()` does not save the object.

## 7. Testing a page with the client
The client sends requests, and the response tells you what happened:

```python
def test_the_book_list_page_shows_each_title(client, db):
    BookFactory(title="Dune")
    response = client.get(reverse("library:book_list"))
    assert response.status_code == 200
    assert b"Dune" in response.content
    assert "library/book_list.html" in [t.name for t in response.templates]
```

`response.templates` lists the templates that were used. `response.json()` decodes a JSON response. `response.context` holds the data the view passed to the template, for example `response.context["books"]`.

For a logged-in page, use `admin_client`, or call `client.force_login(user)` in your own fixture.

## 8. Count the queries
A page that works for one book and fails for a thousand usually has an N+1 problem (module 02). A query-count test catches it before users do:

```python
def test_the_book_list_runs_two_queries_however_many_books(client, db, django_assert_num_queries):
    BookFactory.create_batch(20)
    with django_assert_num_queries(2):
        client.get(reverse("library:book_list"))
```

Count only the request. Build the data before the `with` block, or the count includes the setup.

## 9. Change settings for one test
The `settings` fixture changes a setting for the length of one test, and puts it back afterwards:

```python
def test_the_static_url_follows_the_setting(client, settings, db):
    settings.STATIC_URL = "/assets/"
    response = client.get(reverse("library:book_list"))
    assert b"/assets/library/site.css" in response.content
```

## 10. What to test, and what not to
- Test behaviour: what the user sees, what the API returns, what changes in the database. Do not test that Django saves a row.
- One reason to fail per test. If a test checks five things, a failure does not say which one broke.
- Give each test a name that says the rule, for example `test_a_reader_cannot_review_the_same_book_twice`.
- Pass dates and times into the code. Do not read the current time inside the code under test, or the test changes meaning every day.
- Make the expected values explicit. `assert total == 2800` says more than `assert total == compute_total()`.

## 11. Coverage is a question, not an answer
`pytest --cov=circles --cov-report=term-missing` (after `pip install pytest-cov`) shows which lines no test runs, in a Missing column with their line numbers. It tells you where you have no tests. It does not tell you whether the tests check anything. A test that runs a line and asserts nothing still covers it. Use coverage to find gaps, then write tests that would fail if the code were wrong.

## 12. Habits
- Write the test before the code, for each rule.
- Use a factory for every object a test needs, and override only what the test is about.
- Use parametrize for a table of cases, and a fixture for setup that many tests share.
- Keep the database fixture where it is needed, and no further.
- Run the whole suite before each commit, with `pytest`.

## Check your understanding
1. What does pytest-django do with each test's database changes, and why does that let tests run in any order?
2. What goes wrong if `pytest.ini` has no `DJANGO_SETTINGS_MODULE` line?
3. What does `ids=` add to a parametrized test?
4. A fixture writes a row, and the test fails with a database-access error. What is missing?
5. Why does `ReviewFactory(book__title="Dune")` change the title of a book it builds, and not of a review?
6. Why must the `django_assert_num_queries` block contain only the request?
7. A test calls `load_books()` and asserts nothing. Coverage shows 100 percent for that line. Why does that not prove the test is good?

## Do the exercises
1. **Setup.** Run `pip install -r requirements.txt`. Write `pytest.ini` (TODO 28). Set `DJANGO_SETTINGS_MODULE` to the settings module that `manage.py` names.
2. **Factories.** Write `GameyaFactory`, `MemberFactory` and `PaymentFactory` in `circles/tests/factories.py` (TODO 29). Read the default values in the TODO. To run only the factory tests, use `pytest circles/tests/test_pytest_suite.py -k factory`. The `-k` option runs the tests whose names contain the word. One of them also uses the `gameya` fixture from TODO 30, so it reports an error until TODO 30 is done. That error is expected at this point.
3. **Fixtures.** Write the fixtures in `circles/tests/conftest.py` (TODO 30). Use `db` where a fixture writes to the database. The staff user must be a superuser, so the admin page opens. A plain staff user does not have the model permissions the admin checks.
4. **Run the file.** Run `pytest circles/tests/test_pytest_suite.py`. Stop when all 26 tests pass.
5. **Run everything.** Run `pytest` in `django/gameya_site`. The tests from earlier modules run under pytest too. Some may fail if an earlier module is still a stub, and that is expected until you finish it.
6. **Try a failure on purpose.** Change one value in `Member.due()`, run the tests, and read the failure. Then undo the change.

**Stretch (not tested):** write one parametrized test for the audit log from module 07. Give it three cases: a payment created, a payment deleted, and a member deleted. Check each case's entry with the factories.

**Project step:** the Gameya project now has a pytest suite that builds its data with factories, and that checks the pages, the API and the query counts. Module 09 (caching and performance) uses the query-count tests to measure its changes.

## Exit checklist
- [ ] `pytest circles/tests/test_pytest_suite.py` passes all 26 tests.
- [ ] You can say what the `db`, `client`, `settings` and `django_assert_num_queries` fixtures each give a test.
- [ ] You can say why a test that needs no database should not ask for `db`.
- [ ] You can say what `ids=` and `factory.Sequence` each add.
