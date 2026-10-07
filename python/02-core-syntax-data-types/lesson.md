# Module 02: Core syntax & data types

Python 3.12. Type every example in the REPL. Predict first.

## 1. Variables are names, not boxes
```python
x = 10
y = x
x = 20
print(y)  # 10
```
`x = 10` makes the **name** `x` point at an int object. `y = x` makes `y` point at the same object. Rebinding `x` does not change `y`. (This matters a lot in Module 03 with lists.)

Use `id(x)` to see an object's identity, and `type(x)` for its type.

**Dynamic typing:** names have no type, objects do. `x = 10` then `x = "ten"` is legal.

## 2. Numbers
- `int` has unlimited size: `2 ** 200` works.
- `float` is a 64-bit binary float: `0.1 + 0.2` is `0.30000000000000004`. Never compare floats with `==`; use `math.isclose(a, b)`.
- Operators: `+ - * / // % **`. `/` always gives a float, `//` is floor division, `%` is remainder.
- `round(2.675, 2)` gives `2.67` (float representation). For money, use `decimal.Decimal` or integer piasters.
- Underscores for readability: `1_000_000`.

```python
divmod(17, 5)  # (3, 2)
abs(-4), min(3, 9), max(3, 9), sum([1, 2, 3])
int("42"), float("3.5"), str(99)
```

## 3. Strings (`str`)
Immutable sequences of Unicode characters. Arabic works out of the box.
```python
s = "Gameya جمعية"
len(s)
s.upper(), s.lower(), s.strip(), s.replace("a", "A")
s.split(" ")  # ['Gameya', 'جمعية']
"-".join(["a", "b"])  # 'a-b'
s.startswith("Ga"), "mey" in s
s.find("m"), s.count("a")
```
- **Indexing and slicing:** `s[0]`, `s[-1]`, `s[0:3]`, `s[::2]`, `s[::-1]`. A slice is `[start:stop:step]`, `stop` excluded.
- **Immutable:** `s[0] = "X"` raises `TypeError`. Methods return a **new** string.
- **f-strings:** `f"{name:>10}"`, `f"{price:,.2f}"` gives `1,234.50`, `f"{x=}"` prints `x=5`.
- Multi-line: triple quotes. Raw strings: `r"C:\new"` (backslashes are not escapes).

## 4. Booleans and comparison
- `True` and `False` (capitalised). `bool` is a subclass of `int`: `True + True == 2`.
- Comparisons: `== != < <= > >=`, chainable: `0 < x < 10`.
- `and`, `or`, `not` short-circuit and return one of their operands: `"" or "default"` gives `"default"`.
- **Truthiness:** falsy values are `False, None, 0, 0.0, "", [], (), {}, set()`. Everything else is truthy. So `if items:` means "if not empty".
- `==` compares **value**; `is` compares **identity** (same object). Use `is` only for `None`: `if x is None:`.

## 5. None
`None` means "no value". It is the only value of type `NoneType`. A function without `return` returns `None`.

## 6. Type conversion and checking
```python
int("12"), float("1.5"), str(12), bool("")  # bool("") is False
int("abc")  # ValueError
isinstance(5, int)  # True (prefer over type(x) == int)
```

## 7. Input and output
```python
print("a", "b", sep="-", end="!\n")
age = int(input("Age? "))  # convert, because input() returns str
```

## 8. Comments and structure
`# one-line comment`. Docstrings (`"""..."""`) describe functions. Python uses **indentation**, not braces.

## Check your understanding
1. Why does `x = 20` not change `y` after `y = x`?
2. Why is `0.1 + 0.2 == 0.3` False, and what do you use instead?
3. What does `"hello"[1:4]` return, and `"hello"[::-1]`?
4. Name 6 falsy values.
5. What is the difference between `==` and `is`?
6. What does `"" or "x"` return, and why?
7. Why can't you change a character inside a string?

Then do `exercises.py`.

## Revision companion (optional)
An interactive summary of this lesson, generated with Google NotebookLM: [Mastering Python 3.12 Core Syntax and Data Types](https://notebooklm.link.google/WGAvifLEKiA1). Use it for a quick recap after you finish the lesson and the exercises. This lesson stays the source of truth; the link is hosted by Google and may change.
