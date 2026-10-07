"""Module 01 exercises. Fill in each TODO, then run:  python 01-environment-tooling/exercises.py"""

import sys


# 1. Return the Python version as a string like "3.12.6" (hint: sys.version_info has .major .minor .micro)
def python_version() -> str:
    # TODO
    ...


# 2. Return True if the code is running inside a virtual environment.
#    Hint: inside a venv, sys.prefix differs from sys.base_prefix.
def in_venv() -> bool:
    # TODO
    ...


# 3. Return a greeting: "Hello, <name>! Your name has <n> letters." (use an f-string)
def greet(name: str) -> str:
    # TODO
    ...


# 4. input() returns a string. Convert the two strings to integers and return their sum.
def add_from_text(a: str, b: str) -> int:
    # TODO
    ...


# 5. Predict first, then fill in the expected values (what do these evaluate to?).
def predictions() -> dict:
    return {
        "10 / 3 is a float": None,  # TODO: replace None with the value of 10 / 3 rounded to 2 decimals via round(...)
        "10 // 3": None,  # TODO
        "10 % 3": None,  # TODO
        "2 ** 10": None,  # TODO
        '"ab" * 3': None,  # TODO
    }


if __name__ == "__main__":
    v = python_version()
    assert v.count(".") == 2 and v[0] == "3", "python_version should look like '3.12.6'"
    assert v == f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    assert isinstance(in_venv(), bool), "in_venv should return True or False"

    assert greet("Mohamed") == "Hello, Mohamed! Your name has 7 letters."
    assert greet("Li") == "Hello, Li! Your name has 2 letters."

    assert add_from_text("20", "22") == 42
    assert add_from_text("-5", "5") == 0

    p = predictions()
    assert p["10 / 3 is a float"] == 3.33
    assert p["10 // 3"] == 3
    assert p["10 % 3"] == 1
    assert p["2 ** 10"] == 1024
    assert p['"ab" * 3'] == "ababab"

    print("All checks passed")
    print("Inside a venv?", in_venv(), "(activate .venv and run again to see True)")
