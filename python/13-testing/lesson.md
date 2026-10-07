# Module 13: Testing with pytest

By the end you can write clear, reliable tests: parametrized cases, fixtures, temporary files, mocks and monkeypatching, and you can tell whether your tests are actually any good.

## 1. Why test
Tests prove the code does what you think, and they let you change it later without fear. They are also the fastest way to learn how your own code behaves. Every exercise in this repo has checks; now you write your own.

## 2. Your first test
```python
# test_math.py
def add(a, b):
    return a + b


def test_add():
    assert add(2, 3) == 5
```
Run it:
```bash
pip install pytest
pytest                 # finds test_*.py files and test_* functions
pytest -q              # quiet
pytest path/to/test_file.py::test_name     # one test
pytest -k "total"      # tests whose name contains "total"
pytest -x              # stop at the first failure
```
pytest rewrites `assert` so a failure shows both sides and a diff. No special assert methods needed.

## 3. Test layout: arrange, act, assert
```python
def test_total_adds_every_entry():
    ledger = Ledger()  # arrange
    ledger.add("Ali", 100)
    ledger.add("Sara", 50)

    result = ledger.total()  # act

    assert result == 150  # assert
```
- Name tests for the behaviour: `test_total_adds_every_entry`, not `test_total`.
- One reason to fail per test. Several asserts about the same behaviour are fine.
- Test **behaviour** (inputs and outputs), not how the code is written inside.
- Include edge cases: empty, zero, one, many, the boundary, wrong types, bad input.

## 4. Testing errors
```python
import pytest


def test_rejects_zero():
    with pytest.raises(ValueError, match="positive"):
        Ledger().add("Ali", 0)
```
`match` checks the message (a regular expression). Always check *which* error, not just that something raised.

## 5. Parametrize: many cases, one test
```python
@pytest.mark.parametrize(
    ("text", "cents"),
    [
        ("10", 1000),
        ("1,250.50", 125050),
        ("  7.5 ", 750),
    ],
)
def test_parse_amount(text, cents):
    assert parse_amount(text) == cents
```
Each row is reported separately. Add `ids=[...]` for readable names. Use it for tables of inputs and expected outputs.

## 6. Fixtures: setup you reuse
```python
@pytest.fixture
def ledger():
    ledger = Ledger()
    ledger.add("Ali", 100)
    ledger.add("Sara", 50)
    return ledger


def test_total(ledger):  # pytest passes the fixture in by name
    assert ledger.total() == 150
```
- Every test gets a **fresh** result, so tests cannot affect each other.
- Cleanup with `yield`:
  ```python
  @pytest.fixture
  def connection():
      conn = open_connection()
      yield conn
      conn.close()
  ```
- Share fixtures across files in a `conftest.py`. Scopes: `function` (default), `module`, `session`.
- Built-ins you will use constantly: `tmp_path` (a temporary folder), `monkeypatch`, `capsys` (capture `print`), `caplog` (capture logs).

## 7. Files: `tmp_path`
```python
def test_load(tmp_path):
    file = tmp_path / "ledger.json"
    file.write_text('{"entries": [["Ali", 100]]}', encoding="utf-8")
    assert load_ledger(file).total() == 100
```
Never touch real files in tests. `tmp_path` is created and cleaned for you.

## 8. Replacing things: `monkeypatch` and mocks
Code that depends on the clock, the network or the environment is hard to test. **Replace the dependency** for the length of one test.

**Dependency injection (best):** pass the dependency in, and pass a fake in tests.
```python
def convert(cents, currency, fetch_rate):  # fetch_rate may call the network
    ...


assert convert(1000, "USD", lambda c: 0.0319) == 32
```
**`monkeypatch`:** swap a name for one test, restored automatically.
```python
import payments


def test_label(monkeypatch):
    monkeypatch.setattr(payments, "_today", lambda: date(2026, 10, 10))
    assert today_label() == "Saturday 10 October 2026"


monkeypatch.setenv("API_KEY", "test")
monkeypatch.delenv("API_KEY", raising=False)
```
**`unittest.mock.Mock`:** a fake that records how it was used.
```python
from unittest.mock import Mock

rate = Mock(return_value=0.5)
assert convert(100, "USD", rate) == 50
rate.assert_called_once_with("USD")  # it was called once, with this argument
```
Mock how a collaborator is **called**, assert on results of your own code. Do not mock the thing you are testing.

## 9. Skip, xfail and markers
```python
@pytest.mark.skip(reason="needs the network")
@pytest.mark.skipif(sys.platform == "win32", reason="posix only")
@pytest.mark.xfail(reason="known bug #12")
```
Custom markers (`@pytest.mark.slow`) let you run groups: `pytest -m "not slow"`.

## 10. Are my tests any good? Coverage and mutation
- **Coverage** (`pip install pytest-cov`, `pytest --cov=payments --cov-report=term-missing`) shows which lines ran. 100% coverage does not mean the tests are good; it only means every line executed.
- **Mutation testing** asks the better question: if I plant a bug, does a test fail? `check_tests.py` in this folder does exactly that. A bug that no test notices is a hole in your tests.

## 11. The test-first loop (TDD)
1. Write a failing test for the next small behaviour.
2. Write the least code that makes it pass.
3. Refactor with the tests green.
Use it for new logic and for bug fixes: reproduce the bug in a test first, then fix it.

## 12. What to aim for
- **Fast and independent:** any test can run alone, in any order.
- **Deterministic:** no dependence on today's date, randomness or the network (inject or patch them).
- **Readable:** a failing test should tell you what broke without opening the code.
- Many small unit tests, fewer integration tests, a handful of end-to-end tests. Your Gameya app has 152 end-to-end browser tests; unit tests like these sit underneath them.

## Check your understanding
1. How does pytest find tests, and why does a failing `assert` show so much detail?
2. Why check the error message with `match` and not only the exception type?
3. When do you use `parametrize`, and when a fixture?
4. What does `tmp_path` give you, and why is it better than a real file?
5. Dependency injection, `monkeypatch` and `Mock`: when do you pick each?
6. Why is 100% coverage not proof of good tests? What does mutation testing add?

## Do the exercises
1. Read `payments.py` (do not change it).
2. Write the ten tests in `test_payments.py` and make them pass: `pytest python/13-testing/test_payments.py`.
3. Run `python python/13-testing/check_tests.py`. It plants eight bugs and tells you which ones your tests miss. Fix the gaps until every bug is **caught**.
