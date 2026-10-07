# Module 05: Functions

By the end you can write functions with flexible parameters, explain scope and closures, and use functions as values.

## 1. Defining and calling
```python
def greet(name):
    """Return a greeting."""
    return f"Hello, {name}!"


message = greet("Sara")
```
- `def` creates a function object and binds it to a name. Nothing inside runs until you call it.
- `return` sends a value back and ends the function. No `return` (or a bare `return`) gives `None`.
- The first string is the **docstring**; `help(greet)` shows it.
- Return several values by returning a tuple and unpacking: `low, high = min_max(nums)`.

## 2. Parameters
```python
def pay(amount, currency="EGP", *, fee=0):  # default, keyword-only
    return f"{amount + fee} {currency}"


pay(100)  # positional
pay(100, "USD")  # positional
pay(100, currency="USD")  # keyword
pay(100, fee=5)  # fee must be passed by keyword (it is after the *)
```
- **Positional** arguments match by order; **keyword** arguments match by name.
- **Defaults** are evaluated **once**, when the function is defined. That is the source of the classic bug:

```python
def add(item, bucket=[]):  # WRONG: one shared list for every call
    bucket.append(item)
    return bucket


def add(item, bucket=None):  # RIGHT
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```
Use `None` as the default for anything mutable, and create the object inside.

### `*args` and `**kwargs`
```python
def total(*nums):  # nums is a tuple of the extra positionals
    return sum(nums)


def show(**options):  # options is a dict of the extra keywords
    return ", ".join(f"{k}={v}" for k, v in sorted(options.items()))


total(1, 2, 3)  # 6
show(color="red", size=3)  # 'color=red, size=3'

nums = [1, 2, 3]
total(*nums)  # unpack a sequence into arguments
show(**{"a": 1})  # unpack a dict into keyword arguments
```
Order in a signature: positional, `*args`, keyword-only, `**kwargs`.

## 3. Arguments are passed by object reference
A function receives the **same objects** the caller passed (the names in Module 02 again).
- Mutating a list inside a function changes the caller's list.
- Rebinding the parameter name (`x = x + 1`) does not touch the caller's variable.

Prefer **pure** functions: they compute a result from their inputs and change nothing else. They are easy to test and reason about. Keep input/output (`print`, `input`, files) in a thin layer around them.

## 4. Scope: LEGB
Python looks up a name in this order: **L**ocal, **E**nclosing function, **G**lobal (module), **B**uilt-in.
```python
x = "global"


def outer():
    x = "enclosing"

    def inner():
        x = "local"  # assigning creates a new local name
        return x

    return inner(), x


x = 10


def bump():
    global x  # rebind the module-level name (avoid when you can)
    x += 1
```
Assigning to a name anywhere in a function makes it local for the **whole** function. Reading before assigning raises `UnboundLocalError`.

## 5. Functions are values (first-class)
```python
def square(n):
    return n * n


f = square  # no parentheses: the function itself
f(4)  # 16
ops = {"sq": square, "neg": lambda n: -n}
ops["sq"](5)


def apply(func, value):  # pass a function as an argument
    return func(value)


sorted(["bb", "a", "ccc"], key=len)
sorted(people, key=lambda p: p["age"])
list(map(str.upper, ["a", "b"]))  # prefer comprehensions
```
A `lambda` is a one-expression anonymous function. Use it for short `key=` functions; use `def` for anything longer.

## 6. Closures
An inner function can remember variables from the function that created it, even after that function has returned.
```python
def make_multiplier(n):
    def multiply(x):
        return x * n  # n is remembered

    return multiply


double = make_multiplier(2)
double(21)  # 42


def make_counter():
    count = 0

    def counter():
        nonlocal count  # rebind the enclosing variable
        count += 1
        return count

    return counter
```
Closures are the basis for decorators (Module 10).

## 7. Recursion
A function that calls itself, with a **base case** that stops it.
```python
def factorial(n):
    if n <= 1:  # base case
        return 1
    return n * factorial(n - 1)
```
Python limits recursion depth (about 1000), so use loops for long iterations. Recursion fits tree-shaped data such as nested lists or folders.

## 8. Type hints (preview; Module 11 covers them)
```python
def due(shares: int, share_value: int) -> int:
    return shares * share_value
```
Hints document intent and help your editor; Python does not enforce them at runtime.

## Check your understanding
1. Why is `def f(x, items=[])` a bug waiting to happen? What is the fix?
2. What do `*args` and `**kwargs` hold inside the function?
3. What does `LEGB` stand for, and what happens when you assign to a name inside a function?
4. When do you need `nonlocal`?
5. What is a closure? Give an example from memory.
6. What is the base case of a recursive function and why does it matter?
7. What makes a function "pure"?

Then do `exercises.py`.
