# Module 08: Error handling

By the end you can handle, raise and define exceptions properly, and write code that cleans up after itself.

## 1. What an exception is
When something goes wrong, Python **raises** an exception object. If nothing **catches** it, the program stops and prints a traceback (Module 01: read it from the bottom).

```python
int("abc")  # ValueError
[1, 2][5]  # IndexError
{"a": 1}["b"]  # KeyError
10 / 0  # ZeroDivisionError
None.upper()  # AttributeError
"a" + 1  # TypeError
open("nope.txt")  # FileNotFoundError
```

## 2. try / except / else / finally
```python
try:
    value = int(text)
except ValueError:
    print("not a number")
else:
    print("converted:", value)  # runs only if the try block raised nothing
finally:
    print("always runs")  # cleanup, whatever happened
```
- Catch the **most specific** exception you can handle. `except ValueError:` good; `except Exception:` rarely; a bare `except:` almost never (it also catches `KeyboardInterrupt`).
- Keep the `try` block small: only the line(s) that can fail.
- Several handlers: `except (ValueError, TypeError):` or separate `except` blocks, most specific first.
- Get the object: `except ValueError as e: print(e)`.

## 3. The exception hierarchy
Exceptions are classes. `Exception` is the base of the ones you normally handle; `ValueError`, `KeyError` and `FileNotFoundError` all inherit from it (`KeyError` from `LookupError`, `FileNotFoundError` from `OSError`). Catching a parent catches its children, which is why order matters.

## 4. Raising exceptions
```python
def set_age(age):
    if not 0 <= age <= 120:
        raise ValueError(f"age must be between 0 and 120, got {age}")
    return age


try:
    ...
except KeyError as e:
    raise RuntimeError("config is missing a key") from e  # keep the original as the cause
```
- `raise` inside an `except` block with no argument re-raises the current exception.
- `assert` is for checking your own assumptions during development, not for validating user input (asserts can be switched off).

## 5. Custom exceptions
```python
class GameyaError(Exception):
    """Base class for errors in this app."""


class InsufficientFunds(GameyaError):
    def __init__(self, needed, available):
        super().__init__(f"need {needed}, have {available}")
        self.needed = needed
        self.available = available
```
A base class for your package lets callers catch "anything from my library" with one `except`. Give exceptions useful attributes, not just text.

## 6. EAFP vs LBYL
- **LBYL** ("look before you leap"): `if key in d: value = d[key]`.
- **EAFP** ("easier to ask forgiveness than permission"): `try: value = d[key] except KeyError: ...`.
Python style leans on EAFP when failure is rare or checking is racy (files). For plain dicts, `d.get(key, default)` is simplest.

## 7. Context managers and `with`
`with` guarantees cleanup, even if an exception happens inside.
```python
with open("data.txt", encoding="utf-8") as f:
    text = f.read()
# the file is closed here, always
```
Write your own as a class:
```python
class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self.start
        return False  # False: do not swallow exceptions; True would suppress them
```
Or with a generator:
```python
from contextlib import contextmanager


@contextmanager
def changed_dir(path):
    old = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)
```
Also useful: `contextlib.suppress(FileNotFoundError)`.

## 8. Logging instead of print
```python
import logging

log = logging.getLogger(__name__)
log.warning("payment %s is late", payment_id)
log.exception("could not save")  # inside except: logs the traceback
```
Use `print` for the program's output; use logging for diagnostics.

## 9. Good habits
- Fail early with clear messages. Validate inputs at the edges.
- Don't hide errors with `except: pass`.
- Don't use exceptions for normal control flow in hot loops (they are fine for the "rare failure" case).
- Clean up with `finally` or `with`, not by hoping nothing fails.

## Check your understanding
1. What is the difference between `else` and `finally` in a `try`?
2. Why is a bare `except:` a bad idea?
3. When do you write `raise ... from e`?
4. What are `__enter__` and `__exit__` for, and what does returning `True` from `__exit__` do?
5. Name one case where EAFP is better than an `if` check.
6. Why make a base exception class for your own package?

Then do `exercises.py`.
