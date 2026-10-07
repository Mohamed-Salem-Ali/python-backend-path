"""Part A of the week 1 project. See README.md in this folder."""


def count_words(text: str) -> dict:
    """Return {word: times}, ignoring case and punctuation."""
    # TODO
    ...


def top_words(counts: dict, n: int) -> list:
    """Return the n most common words as (word, count), ties in alphabetical order."""
    # TODO
    ...


if __name__ == "__main__":
    counts = count_words("The cat and the hat. The end!")
    assert counts == {"the": 3, "cat": 1, "and": 1, "hat": 1, "end": 1}
    assert top_words(counts, 2) == [("the", 3), ("and", 1)]
    assert count_words("") == {}
    print("All checks passed")
