"""Module 11 exercises. Add the annotations, then run:  python python/11-typing/exercises.py

The checks read your annotations with typing.get_type_hints, and also run the functions.
Afterwards run a real type checker on the file:  pip install mypy  then  mypy exercises.py
"""

from collections.abc import Callable, Iterable, Sequence
from typing import Literal, Protocol, TypedDict, get_args, get_type_hints


# 1. Annotate: two ints in, an int out.
def add(a, b):
    return a + b


# 2. Annotate: a str, a bool flag with a default, and a str result.
def greet(name, excited=False):
    return f"Hello, {name}{'!' if excited else '.'}"


# 3. Annotate: takes a list of ints, returns an int or None for an empty list.
def first_or_none(items):
    return items[0] if items else None


# 4. Annotate: accepts any sequence of floats, returns a float.
def average(nums):
    return sum(nums) / len(nums)


# 5. Annotate: a list of strings in, a dict from each string to its length out.
def word_lengths(words):
    return {w: len(w) for w in words}


# 6. Annotate: func is a callable taking an int and returning an int.
def apply_twice(func, x):
    return func(func(x))


# 7. Define a TypedDict called MemberRecord with: name (str), shares (int), tags (list of str).
#    Then annotate total_shares to take a list of MemberRecord and return an int.
class MemberRecord(TypedDict):
    # TODO
    ...


def total_shares(members):
    return sum(m["shares"] for m in members)


# 8. Define a Protocol called Payable with a method due(self, share_value: int) -> int.
#    Then annotate total_due: any iterable of Payable and an int in, an int out.
class Payable(Protocol):
    # TODO
    ...


def total_due(items, share_value):
    return sum(item.due(share_value) for item in items)


# 9. A generic function (Python 3.12 syntax: def last[T](...)). Takes a Sequence[T], returns a T.
def last(items):
    return items[-1]


# 10. A generic class Box[T] that stores one item. Methods: get() -> T, set(item: T) -> None.
class Box:
    def __init__(self, item):
        self._item = item

    def get(self):
        return self._item

    def set(self, item):
        self._item = item


# 11. Define Status as a Literal of exactly "paid", "advance", "unpaid", "upcoming".
#     Annotate is_settled to take a Status and return a bool.
Status = None  # TODO


def is_settled(status):
    return status in ("paid", "advance")


# 12. Annotate: takes a str or None, returns an int. (Return 0 for None.)
def safe_len(text):
    return 0 if text is None else len(text)


if __name__ == "__main__":
    assert get_type_hints(add) == {"a": int, "b": int, "return": int}
    assert get_type_hints(greet) == {"name": str, "excited": bool, "return": str}
    assert get_type_hints(first_or_none) == {"items": list[int], "return": int | None}
    h = get_type_hints(average)
    assert h["return"] is float and h["nums"] == Sequence[float], h
    assert get_type_hints(word_lengths) == {
        "words": list[str],
        "return": dict[str, int],
    }
    h = get_type_hints(apply_twice)
    assert h["func"] == Callable[[int], int] and h["x"] is int and h["return"] is int, h

    assert MemberRecord.__annotations__ == {"name": str, "shares": int, "tags": list[str]}
    member: MemberRecord = {"name": "Ali", "shares": 2, "tags": []}
    h = get_type_hints(total_shares)
    assert h["members"] == list[MemberRecord] and h["return"] is int, h
    assert total_shares([member, {"name": "Sara", "shares": 1, "tags": []}]) == 3

    assert getattr(Payable, "_is_protocol", False), "Payable must be a Protocol"
    assert hasattr(Payable, "due")

    class Member:
        def __init__(self, shares: int):
            self.shares = shares

        def due(self, share_value: int) -> int:
            return self.shares * share_value

    h = get_type_hints(total_due)
    assert h["items"] == Iterable[Payable] and h["share_value"] is int and h["return"] is int, h
    assert total_due([Member(2), Member(1)], 100) == 300

    h = get_type_hints(last)
    assert last.__type_params__, "last must be generic: def last[T](...)"
    T = last.__type_params__[0]
    assert h == {"items": Sequence[T], "return": T}, h
    assert last([1, 2, 3]) == 3 and last("abc") == "c"

    assert Box.__type_params__, "Box must be generic: class Box[T]:"
    BT = Box.__type_params__[0]
    assert get_type_hints(Box.get) == {"return": BT}
    assert get_type_hints(Box.set) == {"item": BT, "return": type(None)}
    box = Box(1)
    box.set(5)
    assert box.get() == 5

    assert set(get_args(Status)) == {"paid", "advance", "unpaid", "upcoming"}
    assert get_type_hints(is_settled) == {"status": Status, "return": bool}
    assert is_settled("paid") and not is_settled("unpaid")

    assert get_type_hints(safe_len) == {"text": str | None, "return": int}
    assert safe_len(None) == 0 and safe_len("abc") == 3
    print("All checks passed")
    print("Now run:  mypy exercises.py   (it should report no errors)")
