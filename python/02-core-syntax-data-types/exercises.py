"""Module 02 exercises. Fill the TODOs, run:  python 02-core-syntax-data-types/exercises.py"""

import math


# 1. Return the average of three numbers as a float.
def average3(a: float, b: float, c: float) -> float:
    # TODO
    ...


# 2. Return (quotient, remainder) of a // b without writing // or % (use divmod).
def quot_rem(a: int, b: int) -> tuple:
    # TODO
    ...


# 3. Return True if two floats are equal for practical purposes (hint: math.isclose).
def float_equal(a: float, b: float) -> bool:
    # TODO
    ...


# 4. Return the string reversed, using slicing.
def reverse(s: str) -> str:
    # TODO
    ...


# 5. Return True if s reads the same forwards and backwards, ignoring case and spaces.
def is_palindrome(s: str) -> bool:
    # TODO
    ...


# 6. Format money with thousands separators and 2 decimals plus the currency: money(1234.5) -> "1,234.50 EGP"
def money(amount: float, currency: str = "EGP") -> str:
    # TODO (f-string with :,.2f)
    ...


# 7. Return the first and last character of s as one string; return "" for an empty string.
def ends(s: str) -> str:
    # TODO
    ...


# 8. Return a shortened title: if longer than n characters, cut to n-3 and add "..." (total length n).
def shorten(text: str, n: int) -> str:
    # TODO
    ...


# 9. Return the value if it is not None/empty/zero, otherwise the default. (Use `or`; one line.)
def with_default(value, default):
    # TODO
    ...


# 10. Return how many vowels (a, e, i, o, u, any case) are in s.
def count_vowels(s: str) -> int:
    # TODO
    ...


if __name__ == "__main__":
    assert average3(1, 2, 6) == 3.0
    assert quot_rem(17, 5) == (3, 2)
    assert float_equal(0.1 + 0.2, 0.3) is True
    assert float_equal(1.0, 1.1) is False
    assert reverse("abc") == "cba"
    assert is_palindrome("Never odd or even") is True
    assert is_palindrome("Gameya") is False
    assert money(1234.5) == "1,234.50 EGP"
    assert money(1000000, "USD") == "1,000,000.00 USD"
    assert ends("python") == "pn"
    assert ends("") == ""
    assert ends("x") == "xx"
    assert shorten("Rotating savings circle", 10) == "Rotatin..."
    assert shorten("short", 10) == "short"
    assert with_default("", "n/a") == "n/a"
    assert with_default(0, 5) == 5
    assert with_default("x", "n/a") == "x"
    assert count_vowels("Gameya") == 3
    assert count_vowels("rhythm") == 0
    print("All checks passed")
