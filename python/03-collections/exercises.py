"""Module 03 exercises. Fill the TODOs, run:  python 03-collections/exercises.py"""


# 1. Return a new list with the first and last items swapped. Do not modify the argument.
def swap_ends(items: list) -> list:
    # TODO
    ...


# 2. Return the 3 largest numbers, largest first.
def top3(nums: list) -> list:
    # TODO
    ...


# 3. Append `item` to `items` IN PLACE and return nothing (None). The caller's list must change.
def add_in_place(items: list, item) -> None:
    # TODO
    ...


# 4. Return a NEW list with `item` added. The original must not change.
def add_copy(items: list, item) -> list:
    # TODO
    ...


# 5. Return the min and max of a non-empty list as a tuple (min, max).
def min_max(nums: list) -> tuple:
    # TODO
    ...


# 6. Return the list sorted by string length, longest first.
def by_length(words: list) -> list:
    # TODO (sorted with key=...)
    ...


# 7. Count how many times each word appears. {"a": 2, "b": 1}. Words are lowercase already.
def word_count(words: list) -> dict:
    # TODO
    ...


# 8. Given a dict {name: score}, return the name with the highest score. (max with key=...)
def best(scores: dict) -> str:
    # TODO
    ...


# 9. Invert a dict: {"a": 1, "b": 2} -> {1: "a", 2: "b"}
def invert(d: dict) -> dict:
    # TODO (dict comprehension)
    ...


# 10. Return the unique items, keeping the first-seen order. ([3, 1, 3, 2, 1] -> [3, 1, 2])
def unique_in_order(items: list) -> list:
    # TODO (use a set to remember what you've seen)
    ...


# 11. Return the names that are in BOTH lists, sorted.
def common(a: list, b: list) -> list:
    # TODO (set intersection)
    ...


# 12. Group words by their first letter: ["apple", "avocado", "banana"] -> {"a": ["apple", "avocado"], "b": ["banana"]}
def group_by_first_letter(words: list) -> dict:
    # TODO (setdefault or get)
    ...


if __name__ == "__main__":
    a = [1, 2, 3]
    assert swap_ends(a) == [3, 2, 1] and a == [1, 2, 3]
    assert top3([5, 1, 9, 3, 7]) == [9, 7, 5]

    lst = [1]
    assert add_in_place(lst, 2) is None and lst == [1, 2]
    lst2 = [1]
    out = add_copy(lst2, 2)
    assert out == [1, 2] and lst2 == [1]

    assert min_max([4, 2, 9]) == (2, 9)
    assert by_length(["aa", "b", "cccc"]) == ["cccc", "aa", "b"]
    assert word_count(["a", "b", "a"]) == {"a": 2, "b": 1}
    assert best({"Ali": 7, "Sara": 9, "Omar": 5}) == "Sara"
    assert invert({"a": 1, "b": 2}) == {1: "a", 2: "b"}
    assert unique_in_order([3, 1, 3, 2, 1]) == [3, 1, 2]
    assert common(["ali", "sara", "omar"], ["omar", "mona", "ali"]) == ["ali", "omar"]
    assert group_by_first_letter(["apple", "avocado", "banana"]) == {
        "a": ["apple", "avocado"],
        "b": ["banana"],
    }
    print("All checks passed")
