# Module 07: Object-oriented programming

By the end you can model a problem with classes, explain inheritance and the method resolution order, and use Python's special methods so your objects behave like built-in types.

## 1. Classes and objects
A **class** is a blueprint; an **object** (instance) is one thing built from it. State lives in attributes; behaviour lives in methods.

```python
class Member:
    def __init__(self, name, shares=1):  # runs when you create an instance
        self.name = name  # instance attributes
        self.shares = shares

    def due(self, share_value):  # a method: the first parameter is the instance
        return self.shares * share_value


ali = Member("Ali", 2)
ali.due(100)  # 200: Python passes `ali` as `self`
```
- `self` is just a name for the instance the method was called on.
- `__init__` is the initialiser, not a constructor; the object already exists when it runs.
- Everything is public by convention. A leading underscore (`_cache`) means "internal, please don't touch". A double underscore (`__x`) triggers name mangling and is rarely needed.

## 2. Instance vs class attributes
```python
class Ticket:
    count = 0  # class attribute: shared by all instances

    def __init__(self):
        Ticket.count += 1
        self.id = Ticket.count  # instance attribute: one per object
```
Read a class attribute through the class (`Ticket.count`). Assigning `self.count = ...` would create a separate instance attribute that hides it.

## 3. Readable objects: `__repr__` and `__str__`
```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):  # for developers, ideally valid Python
        return f"Point({self.x}, {self.y})"

    def __str__(self):  # for users; falls back to __repr__
        return f"({self.x}, {self.y})"
```
Always write `__repr__`: it is what you see in the REPL, in tracebacks and in test failures.

## 4. Equality and hashing
By default two instances are equal only if they are the same object. Define `__eq__` to compare by value.
```python
def __eq__(self, other):
    if not isinstance(other, Point):
        return NotImplemented
    return (self.x, self.y) == (other.x, other.y)


def __hash__(self):  # needed to use instances in sets or as dict keys
    return hash((self.x, self.y))
```
If you define `__eq__` without `__hash__`, instances become unhashable. Objects that can change should not be hashable.

## 5. Properties: attributes with logic
```python
class Account:
    def __init__(self):
        self._balance = 0

    @property
    def balance(self):  # read like an attribute: acct.balance
        return self._balance

    @balance.setter
    def balance(self, value):  # acct.balance = 5
        if value < 0:
            raise ValueError("balance cannot be negative")
        self._balance = value
```
A property lets you start with a plain attribute and add validation or a computed value later without changing how callers use it. A property with no setter is read-only.

## 6. `@classmethod` and `@staticmethod`
```python
class Money:
    def __init__(self, cents, currency):
        self.cents, self.currency = cents, currency

    @classmethod
    def from_string(cls, text):  # an alternative constructor
        amount, currency = text.split()
        return cls(round(float(amount) * 100), currency)

    @staticmethod
    def is_valid_currency(code):  # no self or cls: just a function that lives here
        return len(code) == 3 and code.isalpha()
```
`cls` is the class itself, so subclasses get the right type back. Use a `@staticmethod` only when the function belongs with the class conceptually; otherwise a module-level function is fine.

## 7. Inheritance
```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

    def describe(self):
        return f"{self.name} says {self.speak()}"


class Dog(Animal):
    def speak(self):  # override
        return "Woof"


class Puppy(Dog):
    def __init__(self, name, age):
        super().__init__(name)  # run the parent's __init__
        self.age = age
```
- `isinstance(obj, Animal)` is true for every subclass instance; `issubclass(Dog, Animal)` checks classes.
- `describe` calls `self.speak()`, so each subclass changes the result without rewriting `describe`. This is **polymorphism**.
- Python favours **duck typing**: if an object has the method you call, it works, whatever its class.

### Multiple inheritance and the MRO
A class can have several parents. Python decides the lookup order with the **method resolution order** (MRO), a linearisation that keeps parents after children.
```python
class A: ...


class B(A): ...


class C(A): ...


class D(B, C): ...


D.__mro__  # D, B, C, A, object
```
`super()` follows the MRO, not just "the parent", which is what makes cooperative multiple inheritance work (each class calls `super()` and the chain visits everyone once).

**Mixins** are small classes that add one behaviour and are combined with others:
```python
class JsonMixin:
    def to_json(self):
        return json.dumps(vars(self), sort_keys=True)
```

## 8. Composition over inheritance
Inheritance means "is a"; composition means "has a". Prefer composition when the relationship is "has a" or when you only want to reuse behaviour.
```python
class Gameya:  # a Gameya HAS members; it is not a list of them
    def __init__(self):
        self.members = []
```
Deep inheritance trees get brittle. Keep them shallow.

## 9. Special ("dunder") methods
Implement these and your objects work with Python's syntax and built-ins.

| Method | Enables |
|---|---|
| `__len__` | `len(obj)` |
| `__getitem__` | `obj[i]`, slicing, and simple iteration |
| `__iter__` | `for x in obj` |
| `__contains__` | `x in obj` |
| `__bool__` | `if obj:` (falls back to `__len__`) |
| `__add__`, `__mul__`, `__sub__` | `a + b`, `a * 3`, `a - b` |
| `__lt__` and friends | `<`, sorting (`functools.total_ordering` fills in the rest) |
| `__call__` | `obj(...)` |
| `__enter__`, `__exit__` | `with obj:` (Module 08) |

Return `NotImplemented` (not raise) from binary operators when the other type is unsupported.

## 10. Dataclasses
For classes that mostly hold data, `@dataclass` writes `__init__`, `__repr__` and `__eq__` for you.
```python
from dataclasses import dataclass, field


@dataclass
class Member:
    name: str
    shares: int = 1
    tags: list = field(default_factory=list)  # mutable defaults need default_factory


@dataclass(frozen=True)  # immutable and hashable
class Setup:
    weeks: int
    share_value: int

    def __post_init__(self):  # validate after __init__
        if self.weeks <= 0:
            raise ValueError("weeks must be positive")
```
Use a dataclass for records; use a regular class when behaviour and invariants matter more than the fields.

## 11. Design habits
- Keep classes small and focused. If you can't describe it in one sentence, split it.
- Validate in `__init__` (or `__post_init__`) so an object is never in an invalid state.
- Hide internals behind methods and properties; don't make callers poke at `_private` fields.
- Prefer returning new values from methods over mutating shared state when you can.

## Check your understanding
1. What is the difference between an instance attribute and a class attribute? What happens if you assign `self.count = 5` when `count` is a class attribute?
2. Why should every class have a `__repr__`?
3. If you define `__eq__`, what happens to `__hash__`, and why does it matter?
4. When would you use a property instead of a plain attribute?
5. What does `super()` do, and how is it related to the MRO?
6. When do you choose composition instead of inheritance?
7. What does `@dataclass` generate? Why do you need `default_factory` for a list default?

Then do `exercises.py`.
