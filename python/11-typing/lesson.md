# Module 11: Typing

By the end you can annotate code with type hints, describe shapes with `TypedDict`, `Protocol` and generics, and use a type checker to catch mistakes before you run anything.

## 1. What type hints are
Python is dynamically typed: names have no type, objects do. **Type hints** are optional annotations that describe what you *intend*. Python itself ignores them at runtime; **tools** use them: your editor (autocomplete, warnings), a checker such as `mypy` or `pyright`, and frameworks (FastAPI and Pydantic build validation and docs from them).

```python
def due(shares: int, share_value: int) -> int:
    return shares * share_value


name: str = "Ali"  # a variable annotation
```
Hints do **not** stop `due("a", 2)` from running. A checker flags it before you do.

## 2. The basics
```python
count: int = 0
price: float = 9.99
title: str = "Gameya"
active: bool = True
nothing: None = None
```
Built-in collections are generic, so you say what they contain:
```python
names: list[str] = ["Ali", "Sara"]
scores: dict[str, int] = {"Ali": 7}
point: tuple[int, int] = (3, 4)  # fixed length, one type per position
ids: tuple[int, ...] = (1, 2, 3)  # any length, all ints
seen: set[int] = {1, 2}
```
(Before Python 3.9 you imported `List`, `Dict` and friends from `typing`. Today use the built-ins.)

## 3. Unions and `None`
```python
def find(name: str) -> int | None:  # an int, or None when missing
    ...


value: int | str = 5
```
`X | None` replaces the older `Optional[X]`. The checker makes you handle the `None` case:
```python
member = find("Ali")
member + 1  # error: member may be None
if member is not None:  # narrowing: now the checker knows it is an int
    member + 1
```

## 4. Abstract collection types
Accept the **most general** type your function needs; return a concrete one.
```python
from collections.abc import Sequence, Iterable, Mapping


def average(nums: Sequence[float]) -> float: ...  # needs len() and indexing
def total(items: Iterable[int]) -> int: ...  # only needs to loop
def lookup(table: Mapping[str, int], key: str) -> int: ...
```
Taking `Iterable[int]` means callers can pass a list, a set or a generator.

## 5. Functions as values: `Callable`
```python
from collections.abc import Callable


def apply_twice(func: Callable[[int], int], x: int) -> int:
    return func(func(x))
```
`Callable[[arg types], return type]`.

## 6. `Any`, `object` and casting
`Any` turns checking off for that value (use sparingly, at messy boundaries). `object` means "anything, but I can't use it until I check it". `cast(int, value)` tells the checker "trust me"; it does nothing at runtime.

## 7. `TypedDict`: the shape of a dict
```python
from typing import TypedDict


class MemberRecord(TypedDict):
    name: str
    shares: int
    tags: list[str]


def total_shares(members: list[MemberRecord]) -> int:
    return sum(m["shares"] for m in members)
```
It is a plain `dict` at runtime. Perfect for JSON-shaped data. Use a `dataclass` when you want methods and real objects.

## 8. `Literal` and enums
```python
from typing import Literal

Status = Literal["paid", "advance", "unpaid", "upcoming"]


def is_settled(status: Status) -> bool:
    return status in ("paid", "advance")
```
The checker rejects `is_settled("late")`. For a set of values you also iterate over, use `enum.Enum`.

## 9. `Protocol`: structural typing (typed duck typing)
A protocol says "anything with these methods will do", with no inheritance needed.
```python
from typing import Protocol


class Payable(Protocol):
    def due(self, share_value: int) -> int: ...


def total_due(items: Iterable[Payable], share_value: int) -> int:
    return sum(item.due(share_value) for item in items)
```
Any class with a matching `due` method qualifies, including ones you did not write.

## 10. Generics
A function or class that works for **any** type but keeps it consistent.
```python
from collections.abc import Sequence


def first[T](items: Sequence[T]) -> T:  # Python 3.12 syntax
    return items[0]


first([1, 2])  # the checker knows this is an int
first(["a"])  # ...and this is a str


class Box[T]:
    def __init__(self, item: T) -> None:
        self.item = item

    def get(self) -> T:
        return self.item
```
Before 3.12 you wrote `T = TypeVar("T")` and `class Box(Generic[T])`. You will see both.

## 11. Dataclasses and typing
`@dataclass` uses annotations to build the class (Module 07), so typing and design go together: `name: str`, `shares: int = 1`, `tags: list[str] = field(default_factory=list)`.

## 12. Running a type checker
```bash
pip install mypy
mypy exercises.py              # basic checks
mypy --strict exercises.py     # also demands annotations everywhere
```
A checker reads the code and reports mismatches; it never runs it. You can adopt it gradually: start with `mypy file.py`, add `--strict` for new modules. `pyright` (used inside VS Code's Pylance) works the same way.

## 13. Reading hints at runtime
```python
from typing import get_type_hints

get_type_hints(due)  # {'shares': int, 'share_value': int, 'return': int}
```
This is how FastAPI and Pydantic turn your annotations into validation and OpenAPI docs, which is why typing matters for Phase 2.

## 14. Habits
- Annotate function signatures first; local variables are usually inferred.
- Prefer abstract parameter types, concrete return types.
- Use `X | None` and narrow it, rather than returning sentinel values.
- Keep `Any` out of your core logic.
- Hints describe intent; tests prove behaviour. You need both.

## Check your understanding
1. Does Python enforce type hints at runtime? Who does?
2. What is the difference between `list[int]`, `Sequence[int]` and `Iterable[int]` as a parameter type?
3. What does the checker force you to do with a value of type `int | None`?
4. What does a `Protocol` give you that a base class does not?
5. How do you write a function that returns the same type it received?
6. How does a framework like FastAPI use your annotations?

Then do `exercises.py`.
