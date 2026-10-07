# Module 10: Decorators

By the end you can write decorators (with and without arguments), keep function metadata intact, and recognise the decorators you meet in every Python framework.

## 1. The idea
A **decorator** is a function that takes a function and returns a (usually wrapped) function. This syntax:
```python
@shout
def greet():
    return "hello"
```
is exactly the same as:
```python
def greet():
    return "hello"


greet = shout(greet)
```
It relies on two things you already know: functions are values (Module 05) and closures remember variables (Module 05).

## 2. Your first decorator
```python
def shout(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)  # call the original
        return result.upper()  # change something around it

    return wrapper


@shout
def greet(name):
    return f"hello, {name}"


greet("sara")  # 'HELLO, SARA'
```
Use `*args, **kwargs` in the wrapper so it works with any signature, and always `return` the result.

## 3. Keep the metadata: `functools.wraps`
Without help, the wrapper replaces the function's name and docstring:
```python
greet.__name__  # 'wrapper'  (not 'greet')
```
Fix it with `functools.wraps`:
```python
from functools import wraps


def shout(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()

    return wrapper
```
Always use `@wraps`. It keeps `__name__`, `__doc__` and more, which matters for debugging, documentation and frameworks that inspect functions.

## 4. A wrapper that keeps state
Functions are objects, so you can hang attributes on the wrapper.
```python
def count_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)

    wrapper.calls = 0
    return wrapper
```

## 5. Decorators with arguments (a factory)
When you write `@repeat(3)`, `repeat(3)` runs first and must **return the decorator**. That adds one more level of nesting:
```python
def repeat(times):  # the factory: takes the arguments
    def decorator(func):  # the decorator: takes the function
        @wraps(func)
        def wrapper(*args, **kwargs):  # the wrapper: runs on every call
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result

        return wrapper

    return decorator


@repeat(3)
def ping():
    print("ping")
```
Read it as three layers: configure, receive the function, run.

## 6. Stacking decorators
```python
@bold
@italic
def text():
    return "hi"


# same as: text = bold(italic(text))
```
The one closest to the function is applied first, so `italic` wraps `text` and `bold` wraps that. Order matters.

## 7. Real-world patterns
**Timing**
```python
import time


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            wrapper.last_elapsed = time.perf_counter() - start

    return wrapper
```
**Retry on failure**
```python
def retry(times, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions:
                    if attempt == times:
                        raise

        return wrapper

    return decorator
```
**Access control**: the same idea as `requireAdmin()` on every server action in a web app.
```python
def require_role(role):
    def decorator(func):
        @wraps(func)
        def wrapper(user, *args, **kwargs):
            if user.get("role") != role:
                raise PermissionError(f"{role} role required")
            return func(user, *args, **kwargs)

        return wrapper

    return decorator
```
**Registry**: collect functions by name (a decorator that returns the original function unchanged).
```python
HANDLERS = {}


def register(func):
    HANDLERS[func.__name__] = func
    return func
```
**Caching**: `functools.lru_cache` (Module 06) and `functools.cache` are decorators. Write your own once (a `dict` keyed by the arguments) to understand them.

## 8. Decorators you already use
- `@property`, `@staticmethod`, `@classmethod` (Module 07)
- `@dataclass` (a class decorator: it receives a class and returns it, improved)
- `@contextmanager` (Module 08)
- `@lru_cache`, `@wraps`
- In web frameworks: `@app.get("/items")` (FastAPI), `@login_required` and `@api_view` (Django), `@pytest.fixture`

## 9. Decorating methods and classes
A wrapper that uses `*args` already works on methods: `self` arrives as the first positional argument. A class decorator takes a class and returns a class (often the same one with something added).

## 10. When not to use them
Decorators hide control flow. Use them for behaviour that applies to many functions in the same way (logging, auth, timing, caching, registration). If it only applies to one function, a plain call is clearer.

## Check your understanding
1. What does `@shout` above `def greet` expand to?
2. Why do wrappers take `*args, **kwargs`?
3. What does `functools.wraps` fix, and why does it matter?
4. Why does `@repeat(3)` need three nested functions?
5. In `@bold` over `@italic`, which runs first?
6. Name three decorators you have used without writing them.

Then do `exercises.py`.
