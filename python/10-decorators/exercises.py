"""Module 10 exercises. Fill the TODOs, run:  python python/10-decorators/exercises.py"""

import time
from functools import wraps  # noqa: F401  (you will need this)

CALL_LOG: list = []
REGISTRY: dict = {}


# 1. Make the decorated function return its (string) result in upper case.
def shout(func):
    # TODO
    ...


# 2. Record every call in CALL_LOG as "name(args)", e.g. "add(1, 2)" for add(1, 2) (positional only),
#    and keep the original name and docstring.
def log_calls(func):
    # TODO
    ...


# 3. Count calls in wrapper.calls (starts at 0).
def count_calls(func):
    # TODO
    ...


# 4. A decorator FACTORY: @repeat(3) calls the function three times and returns the last result.
def repeat(times: int):
    # TODO
    ...


# 5. A decorator factory: try the function up to `times` attempts; if every attempt raises one of
#    `exceptions`, raise the LAST exception. Other exceptions are not retried.
def retry(times: int, exceptions: tuple = (Exception,)):
    # TODO
    ...


# 6. Cache results by arguments in wrapper.cache (a dict). Positional arguments only.
def memoize(func):
    # TODO
    ...


# 7. Raise ValueError("arguments must be positive") if any positional argument is <= 0.
def positive_args(func):
    # TODO
    ...


# 8. Stacking. bold wraps a string result in <b>..</b>; italic wraps it in <i>..</i>.
def bold(func):
    # TODO
    ...


def italic(func):
    # TODO
    ...


# 9. Measure how long each call takes (time.perf_counter) and store it in wrapper.last_elapsed.
def timed(func):
    # TODO
    ...


# 10. Add the function to REGISTRY under its own name and return it unchanged.
def register(func):
    # TODO
    ...


# 11. Access control. The decorated function takes `user` (a dict with "role") as its first
#     argument. Raise PermissionError(f"{role} role required") when the role does not match.
def require_role(role: str):
    # TODO
    ...


def check_shout():
    @shout
    def greet(name):
        """Say hello."""
        return f"hello, {name}"

    assert greet("sara") == "HELLO, SARA"
    assert greet.__name__ == "greet" and greet.__doc__ == "Say hello."


def check_log_calls():
    CALL_LOG.clear()

    @log_calls
    def add(a, b):
        """Add two numbers."""
        return a + b

    assert add(1, 2) == 3 and add(3, 4) == 7
    assert CALL_LOG == ["add(1, 2)", "add(3, 4)"], CALL_LOG
    assert add.__name__ == "add" and add.__doc__ == "Add two numbers."


def check_count_calls():
    @count_calls
    def ping():
        return "pong"

    assert ping.calls == 0
    ping()
    ping()
    assert ping.calls == 2 and ping() == "pong"


def check_repeat():
    seen: list = []

    @repeat(3)
    def tick():
        seen.append(1)
        return len(seen)

    assert tick() == 3 and len(seen) == 3


def check_retry():
    attempts: list = []

    @retry(3, exceptions=(ConnectionError,))
    def flaky(succeed_on):
        attempts.append(1)
        if len(attempts) < succeed_on:
            raise ConnectionError(f"attempt {len(attempts)}")
        return "ok"

    assert flaky(3) == "ok" and len(attempts) == 3
    attempts.clear()
    try:
        flaky(99)
    except ConnectionError as e:
        assert str(e) == "attempt 3", str(e)
    else:
        raise AssertionError("retry must re-raise the last error")
    assert len(attempts) == 3

    @retry(5, exceptions=(ConnectionError,))
    def wrong_kind():
        raise KeyError("not retried")

    try:
        wrong_kind()
    except KeyError:
        pass
    else:
        raise AssertionError("KeyError should pass straight through")


def check_memoize():
    calls: list = []

    @memoize
    def slow_square(n):
        calls.append(n)
        return n * n

    assert slow_square(4) == 16 and slow_square(4) == 16 and slow_square(5) == 25
    assert calls == [4, 5] and slow_square.cache[(4,)] == 16


def check_positive_args():
    @positive_args
    def area(w, h):
        return w * h

    assert area(2, 3) == 6
    try:
        area(2, -1)
    except ValueError as e:
        assert str(e) == "arguments must be positive"
    else:
        raise AssertionError("area(2, -1) must raise ValueError")


def check_stacking():
    @bold
    @italic
    def text():
        return "hi"

    assert text() == "<b><i>hi</i></b>"


def check_timed():
    @timed
    def nap():
        time.sleep(0.01)
        return "done"

    assert nap() == "done" and nap.last_elapsed >= 0.01


def check_register():
    REGISTRY.clear()

    @register
    def handler_one():
        return 1

    assert REGISTRY == {"handler_one": handler_one} and handler_one() == 1


def check_require_role():
    @require_role("admin")
    def delete_everything(user, what):
        return f"{user['name']} deleted {what}"

    assert delete_everything({"name": "Ali", "role": "admin"}, "logs") == "Ali deleted logs"
    try:
        delete_everything({"name": "Sara", "role": "member"}, "logs")
    except PermissionError as e:
        assert str(e) == "admin role required"
    else:
        raise AssertionError("members must not be allowed")


if __name__ == "__main__":
    # Run in order, so the first failure points at the first decorator you have not finished.
    for check in (
        check_shout,
        check_log_calls,
        check_count_calls,
        check_repeat,
        check_retry,
        check_memoize,
        check_positive_args,
        check_stacking,
        check_timed,
        check_register,
        check_require_role,
    ):
        check()
    print("All checks passed")
