"""Module 05 exercises. Fill the TODOs, run:  python python/05-functions/exercises.py"""


# 1. Return x limited to the range [low, high].
def clamp(x: float, low: float, high: float) -> float:
    # TODO
    ...


# 2. greet("Sara") -> "Hello, Sara!"   greet("Sara", "Hi") -> "Hi, Sara!"
#    greet("Sara", punctuation=".") -> "Hello, Sara."   (punctuation is keyword-only)
def greet(name: str, greeting: str = "Hello", *, punctuation: str = "!") -> str:
    # TODO
    ...


# 3. Return the sum of any number of arguments. total() -> 0
def total(*nums: float) -> float:
    # TODO
    ...


# 4. Return the options as "a=1, b=2", sorted by key. describe() -> ""
def describe(**options) -> str:
    # TODO
    ...


# 5. Fix the mutable-default trap: add `item` to `bucket` and return it.
#    Without a bucket, start a fresh list on every call.
def add_item(item, bucket=None) -> list:
    # TODO
    ...


# 6. Return a function that returns 1, then 2, then 3... each time it is called (a closure).
def make_counter():
    # TODO
    ...


# 7. make_multiplier(3)(5) -> 15
def make_multiplier(n: float):
    # TODO
    ...


# 8. compose(f, g)(x) -> f(g(x))
def compose(f, g):
    # TODO
    ...


# 9. Sort (name, score) pairs by score, highest first, using sorted with a key.
def by_score(pairs: list) -> list:
    # TODO
    ...


# 10. Recursive factorial. factorial(0) -> 1
def factorial(n: int) -> int:
    # TODO
    ...


# 11. Recursively flatten any depth of nested lists: [1, [2, [3, 4]], 5] -> [1, 2, 3, 4, 5]
def flatten_deep(nested: list) -> list:
    # TODO
    ...


# 12. Apply f to x, n times. apply_n(lambda v: v * 2, 1, 5) -> 32. n=0 returns x.
def apply_n(f, x, n: int):
    # TODO
    ...


# 13. Return a function that remembers how many times it has been called with each argument.
#     counter = make_tally(); counter("a") -> 1; counter("a") -> 2; counter("b") -> 1
def make_tally():
    # TODO (closure over a dict)
    ...


if __name__ == "__main__":
    assert clamp(5, 0, 10) == 5 and clamp(-1, 0, 10) == 0 and clamp(99, 0, 10) == 10

    assert greet("Sara") == "Hello, Sara!"
    assert greet("Sara", "Hi") == "Hi, Sara!"
    assert greet("Sara", punctuation=".") == "Hello, Sara."
    try:
        greet("Sara", "Hi", "?")  # a third positional argument must be rejected
    except TypeError:
        pass
    else:
        raise AssertionError("punctuation must be keyword-only")

    assert total() == 0 and total(1, 2, 3) == 6
    assert describe() == ""
    assert describe(b=2, a=1) == "a=1, b=2"

    first = add_item("x")
    second = add_item("y")
    assert first == ["x"] and second == ["y"], "each call needs its own fresh list"
    mine = ["a"]
    assert add_item("b", mine) is mine and mine == ["a", "b"]

    c = make_counter()
    assert [c(), c(), c()] == [1, 2, 3]
    c2 = make_counter()
    assert c2() == 1, "each counter has its own state"

    assert make_multiplier(3)(5) == 15
    assert compose(lambda v: v + 1, lambda v: v * 2)(5) == 11
    assert by_score([("a", 5), ("b", 9), ("c", 7)]) == [("b", 9), ("c", 7), ("a", 5)]
    assert factorial(0) == 1 and factorial(5) == 120
    assert flatten_deep([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]
    assert flatten_deep([]) == []
    assert apply_n(lambda v: v * 2, 1, 5) == 32 and apply_n(str.upper, "a", 0) == "a"

    t = make_tally()
    assert [t("a"), t("a"), t("b")] == [1, 2, 1]
    print("All checks passed")
