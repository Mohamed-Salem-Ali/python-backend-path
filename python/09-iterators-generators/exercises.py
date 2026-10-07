"""Module 09 exercises. Fill the TODOs, run:  python python/09-iterators-generators/exercises.py"""

from itertools import islice


# 1. A generator that yields n, n-1, ... 1. countdown(0) yields nothing.
def countdown(n: int):
    # TODO
    ...


# 2. The same idea as an iterator CLASS: yields start, start+1, ... stop-1 (like range).
#    Remember __iter__ returns self and __next__ raises StopIteration at the end.
class Span:
    def __init__(self, start: int, stop: int):
        # TODO
        ...

    def __iter__(self):
        # TODO
        ...

    def __next__(self):
        # TODO
        ...


# 3. An infinite generator of Fibonacci numbers: 0, 1, 1, 2, 3, 5, ...
def fibonacci():
    # TODO
    ...


# 4. Yield the first n items of any iterable (do not use itertools).
def take(iterable, n: int):
    # TODO
    ...


# 5. Yield only the even numbers from an iterable, lazily.
def evens(numbers):
    # TODO
    ...


# 6. Yield lists of `size` items; the last one may be shorter. Works on any iterable (a generator
#    has no len() or slicing).
def chunked(iterable, size: int):
    # TODO
    ...


# 7. Flatten one level of nesting with `yield from`: [[1, 2], [3], []] -> 1, 2, 3
def flatten(rows):
    # TODO
    ...


# 8. A text pipeline: yield each non-empty line of `text`, stripped of surrounding spaces.
def clean_lines(text: str):
    # TODO
    ...


# 9. Yield consecutive pairs: [1, 2, 3, 4] -> (1, 2), (2, 3), (3, 4). Fewer than 2 items -> nothing.
def pairs(iterable):
    # TODO
    ...


# 10. A one-liner with a generator expression: the sum of squares of the odd numbers below n.
def sum_odd_squares(n: int) -> int:
    # TODO
    ...


# 11. Yield each item only the first time it appears (lazily, keep a set of what you have seen).
def unique(iterable):
    # TODO
    ...


# 12. Repeat the items `times` times in order: repeat_items([1, 2], 2) -> 1, 2, 1, 2 (use yield from).
def repeat_items(items, times: int):
    # TODO
    ...


if __name__ == "__main__":
    assert list(countdown(3)) == [3, 2, 1] and list(countdown(0)) == []
    assert hasattr(countdown(1), "__next__"), "countdown must be a generator"

    assert list(Span(2, 5)) == [2, 3, 4] and list(Span(3, 3)) == []
    sp = Span(0, 2)
    assert next(sp) == 0 and next(sp) == 1
    try:
        next(sp)
    except StopIteration:
        pass
    else:
        raise AssertionError("Span must raise StopIteration when done")

    assert list(islice(fibonacci(), 8)) == [0, 1, 1, 2, 3, 5, 8, 13]
    assert list(take(fibonacci(), 5)) == [0, 1, 1, 2, 3]
    assert list(take([1, 2], 10)) == [1, 2]
    assert list(evens(range(10))) == [0, 2, 4, 6, 8]
    assert list(take(evens(fibonacci()), 4)) == [0, 2, 8, 34], "evens must be lazy"
    assert list(chunked(iter(range(5)), 2)) == [[0, 1], [2, 3], [4]] and list(chunked([], 3)) == []
    assert list(flatten([[1, 2], [3], []])) == [1, 2, 3]
    assert list(clean_lines("  a  \n\n b\n   \nc")) == ["a", "b", "c"]
    assert list(pairs([1, 2, 3, 4])) == [(1, 2), (2, 3), (3, 4)] and list(pairs([1])) == []
    assert sum_odd_squares(6) == 1 + 9 + 25
    assert list(unique([3, 1, 3, 2, 1])) == [3, 1, 2]
    assert list(repeat_items([1, 2], 2)) == [1, 2, 1, 2] and list(repeat_items([1], 0)) == []

    g = countdown(2)
    assert list(g) == [2, 1] and list(g) == [], "a generator is exhausted after one pass"
    print("All checks passed")
