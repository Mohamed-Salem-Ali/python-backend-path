"""Module 06 exercises. Fill the TODOs, run:  python python/06-modules-packages-stdlib/exercises.py"""

import json
import re
import tempfile
from collections import Counter, defaultdict
from datetime import date, timedelta
from functools import lru_cache
from itertools import accumulate, islice
from pathlib import Path


# 1. Days between two ISO dates ("2026-10-10"), as a positive or negative int (b - a).
def days_between(a: str, b: str) -> int:
    # TODO (date.fromisoformat)
    ...


# 2. The first date on or after `start` that falls on `weekday` (Monday=0 ... Sunday=6).
#    next_weekday("2026-10-05", 5) -> "2026-10-10"  (a Saturday)
def next_weekday(start: str, weekday: int) -> str:
    # TODO
    ...


# 3. The payment window opens on the Sunday on or before the payout day.
#    pay_window_start("2026-10-10") -> "2026-10-04"; for a Sunday payout day it is that same day.
def pay_window_start(payout_day: str) -> str:
    # TODO (hint: date.weekday() gives Mon=0 .. Sun=6; Sunday is 6)
    ...


# 4. The n most common words as (word, count) tuples. No ties in the tests.
def top_words(words: list, n: int) -> list:
    # TODO (Counter.most_common)
    ...


# 5. Group anagrams: ["eat", "tea", "tan", "nat", "bat"] ->
#    [["bat"], ["eat", "tea"], ["nat", "tan"]]. Sort each group, then sort the groups.
def group_anagrams(words: list) -> list:
    # TODO (defaultdict(list) keyed by the sorted letters)
    ...


# 6. Dump a dict as JSON with sorted keys, keeping non-ASCII text readable (no \uXXXX escapes).
def to_json(data: dict) -> str:
    # TODO
    ...


# 7. Return every whole number in the text as an int: "weeks 10 and 12" -> [10, 12]
def extract_numbers(text: str) -> list:
    # TODO (re.findall)
    ...


# 8. Split a list into chunks of `size`: chunk([1, 2, 3, 4, 5], 2) -> [[1, 2], [3, 4], [5]]
def chunk(items: list, size: int) -> list:
    # TODO
    ...


# 9. Running totals: [100, 100, 50] -> [100, 200, 250]
def running_total(nums: list) -> list:
    # TODO (itertools.accumulate)
    ...


# 10. Count file extensions, lowercase, without the dot; files without one are skipped.
#     ["a.PY", "b.py", "c.txt", "README"] -> {"py": 2, "txt": 1}
def extension_counts(filenames: list) -> dict:
    # TODO (pathlib.PurePath(name).suffix)
    ...


# 11. Make this fast with a cache: fib(80) must return instantly.
def fib(n: int) -> int:
    # TODO (add the right decorator, then implement)
    ...


# 12. Write the lines to a file (one per line) and read them back, using pathlib and UTF-8.
def save_and_load(path: Path, lines: list) -> list:
    # TODO (write_text then read_text().splitlines())
    ...


# 13. Return the first n numbers of an endless generator using islice.
def naturals():
    n = 1
    while True:
        yield n
        n += 1


def first_n_naturals(n: int) -> list:
    # TODO
    ...


if __name__ == "__main__":
    assert days_between("2026-10-10", "2026-10-17") == 7
    assert days_between("2026-10-17", "2026-10-10") == -7
    assert next_weekday("2026-10-05", 5) == "2026-10-10"
    assert next_weekday("2026-10-10", 5) == "2026-10-10"
    assert pay_window_start("2026-10-10") == "2026-10-04"
    assert pay_window_start("2026-10-04") == "2026-10-04"
    assert pay_window_start("2026-10-17") == "2026-10-11"

    assert top_words(["a", "b", "a", "c", "a", "b"], 2) == [("a", 3), ("b", 2)]
    assert group_anagrams(["eat", "tea", "tan", "nat", "bat"]) == [
        ["bat"],
        ["eat", "tea"],
        ["nat", "tan"],
    ]
    out = to_json({"b": 1, "a": "جمعية"})
    assert out == '{"a": "جمعية", "b": 1}', out
    assert json.loads(out) == {"a": "جمعية", "b": 1}
    assert extract_numbers("weeks 10 and 12") == [10, 12]
    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]] and chunk([], 3) == []
    assert running_total([100, 100, 50]) == [100, 200, 250]
    assert extension_counts(["a.PY", "b.py", "c.txt", "README"]) == {"py": 2, "txt": 1}
    assert fib(80) == 23416728348467685
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", date(2026, 1, 2).isoformat())
    assert date(2026, 10, 10) + timedelta(days=7) == date(2026, 10, 17)

    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "sub" / "notes.txt"
        target.parent.mkdir()
        assert save_and_load(target, ["أول", "second"]) == ["أول", "second"]

    assert first_n_naturals(4) == [1, 2, 3, 4]
    print("All checks passed")
