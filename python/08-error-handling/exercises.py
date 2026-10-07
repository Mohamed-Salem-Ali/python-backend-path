"""Module 08 exercises. Fill the TODOs, run:  python python/08-error-handling/exercises.py"""

import json
import tempfile
from contextlib import contextmanager
from pathlib import Path


# 1. Convert text to int; return `default` if it is not a valid number.
def safe_int(text: str, default=None):
    # TODO
    ...


# 2. Divide a by b; return None when b is zero.
def safe_divide(a: float, b: float):
    # TODO
    ...


# 3. Parse an age. Non-numbers raise ValueError (the normal int() error is fine).
#    Out-of-range values raise ValueError("age must be between 0 and 120").
def parse_age(text: str) -> int:
    # TODO
    ...


# 4. A custom exception carrying data, and a function that raises it.
class InsufficientFunds(Exception):
    def __init__(self, needed: int, available: int):
        # TODO: call super().__init__ with a message and store both numbers as attributes
        ...


def withdraw(balance: int, amount: int) -> int:
    """Return the new balance, or raise InsufficientFunds(needed=amount, available=balance)."""
    # TODO
    ...


# 5. Read JSON from a file. Missing file -> {}. Invalid JSON -> raise ConfigError from the original.
class ConfigError(Exception):
    pass


def read_config(path: Path) -> dict:
    # TODO
    ...


# 6. Return the first item that can be converted to an int (as an int), or None if none can.
def first_int(values: list):
    # TODO
    ...


# 7. Call each function with no arguments. Return ("ok", result) or ("error", ExceptionClassName)
#    for each one, in order. One failure must not stop the others.
def run_all(funcs: list) -> list:
    # TODO
    ...


# 8. Always log "close", even when the work fails. Let the exception propagate.
#    process(log, fail=False) logs: open, work, close
#    process(log, fail=True)  logs: open, close   and raises RuntimeError
def process(log: list, fail: bool) -> None:
    # TODO (try/finally)
    ...


# 9. A context manager class that records "enter" and "exit" in a log and swallows ValueError only.
class Recorder:
    def __init__(self, log: list):
        self.log = log

    def __enter__(self):
        # TODO
        ...

    def __exit__(self, exc_type, exc, tb):
        # TODO: record "exit"; return True only if exc_type is ValueError (or a subclass)
        ...


# 10. A context manager (use @contextmanager) that sets d[key] = value inside the block and
#     restores the previous state afterwards (remove the key if it was not there before),
#     even if the block raises.
@contextmanager
def temporary_value(d: dict, key, value):
    # TODO
    yield


if __name__ == "__main__":
    assert safe_int("42") == 42 and safe_int("x") is None and safe_int("x", 0) == 0
    assert safe_int("") is None
    assert safe_divide(6, 3) == 2 and safe_divide(1, 0) is None

    assert parse_age("30") == 30
    for bad in ("abc", "-1", "121"):
        try:
            parse_age(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"parse_age({bad!r}) should raise ValueError")
    try:
        parse_age("200")
    except ValueError as e:
        assert str(e) == "age must be between 0 and 120", str(e)

    assert withdraw(100, 30) == 70
    try:
        withdraw(10, 50)
    except InsufficientFunds as e:
        assert e.needed == 50 and e.available == 10
        assert isinstance(e, Exception)
    else:
        raise AssertionError("withdraw should raise InsufficientFunds")

    with tempfile.TemporaryDirectory() as tmp:
        good = Path(tmp) / "good.json"
        good.write_text('{"a": 1}', encoding="utf-8")
        assert read_config(good) == {"a": 1}
        assert read_config(Path(tmp) / "missing.json") == {}
        bad = Path(tmp) / "bad.json"
        bad.write_text("{not json", encoding="utf-8")
        try:
            read_config(bad)
        except ConfigError as e:
            assert isinstance(e.__cause__, json.JSONDecodeError)
        else:
            raise AssertionError("bad JSON should raise ConfigError")

    assert first_int(["a", "7", "9"]) == 7 and first_int(["a", "b"]) is None
    assert run_all([lambda: 1, lambda: 1 / 0, lambda: [][1]]) == [
        ("ok", 1),
        ("error", "ZeroDivisionError"),
        ("error", "IndexError"),
    ]

    log: list = []
    process(log, fail=False)
    assert log == ["open", "work", "close"]
    log = []
    try:
        process(log, fail=True)
    except RuntimeError:
        pass
    else:
        raise AssertionError("process should let RuntimeError propagate")
    assert log == ["open", "close"]

    log = []
    with Recorder(log):
        raise ValueError("swallowed")
    assert log == ["enter", "exit"]
    try:
        with Recorder([]):
            raise KeyError("not swallowed")
    except KeyError:
        pass
    else:
        raise AssertionError("Recorder must not swallow KeyError")

    settings = {"debug": False}
    with temporary_value(settings, "debug", True):
        assert settings["debug"] is True
    assert settings == {"debug": False}
    with temporary_value(settings, "new", 1):
        assert settings["new"] == 1
    assert "new" not in settings
    try:
        with temporary_value(settings, "debug", True):
            raise RuntimeError("boom")
    except RuntimeError:
        pass
    assert settings == {"debug": False}
    print("All checks passed")
