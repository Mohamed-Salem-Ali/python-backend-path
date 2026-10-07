"""Module 07 exercises. Fill the TODOs, run:  python python/07-oop/exercises.py"""

import json
from dataclasses import dataclass, field


# 1. A 2D point. repr -> "Point(1, 2)". Equal when both coordinates match. Hashable.
#    distance_to(other) -> straight-line distance as a float.
class Point:
    def __init__(self, x: float, y: float):
        # TODO
        ...

    def __repr__(self) -> str:
        # TODO
        ...

    def __eq__(self, other):
        # TODO (return NotImplemented for other types)
        ...

    def __hash__(self) -> int:
        # TODO
        ...

    def distance_to(self, other: "Point") -> float:
        # TODO
        ...


# 2. A bank account. `balance` is a read-only property. deposit/withdraw reject amounts <= 0
#    with ValueError; withdraw rejects amounts above the balance with ValueError("insufficient funds").
class BankAccount:
    def __init__(self, opening: int = 0):
        # TODO
        ...

    @property
    def balance(self) -> int:
        # TODO
        ...

    def deposit(self, amount: int) -> None:
        # TODO
        ...

    def withdraw(self, amount: int) -> None:
        # TODO
        ...


# 3. Temperature stored in celsius. `fahrenheit` is a property with a setter that updates celsius.
#    F = C * 9 / 5 + 32
class Temperature:
    def __init__(self, celsius: float):
        # TODO
        ...

    @property
    def fahrenheit(self) -> float:
        # TODO
        ...

    @fahrenheit.setter
    def fahrenheit(self, value: float) -> None:
        # TODO
        ...


# 4. A 2D vector with +, scalar *, abs() (length) and truthiness (the zero vector is falsy).
#    Vector(1, 2) + Vector(3, 4) == Vector(4, 6); Vector(1, 2) * 3 == Vector(3, 6)
@dataclass(frozen=True)
class Vector:
    x: float
    y: float

    def __add__(self, other):
        # TODO
        ...

    def __mul__(self, k):
        # TODO
        ...

    def __abs__(self) -> float:
        # TODO
        ...

    def __bool__(self) -> bool:
        # TODO
        ...


# 5. A stack. push/pop/peek, len(), and truthiness. pop() and peek() on an empty stack raise
#    IndexError("empty stack").
class Stack:
    def __init__(self):
        # TODO
        ...

    def push(self, item) -> None:
        # TODO
        ...

    def pop(self):
        # TODO
        ...

    def peek(self):
        # TODO
        ...

    def __len__(self) -> int:
        # TODO
        ...


# 6. A playlist that behaves like a sequence: len(), indexing, `in`, and iteration.
class Playlist:
    def __init__(self, *songs: str):
        # TODO
        ...

    def __len__(self) -> int:
        # TODO
        ...

    def __getitem__(self, index):
        # TODO
        ...

    def __contains__(self, song) -> bool:
        # TODO
        ...


# 7. Polymorphism. Animal.speak() returns "..."; Dog says "Woof", Cat says "Meow".
#    describe() lives only in Animal: "Rex says Woof".
class Animal:
    def __init__(self, name: str):
        # TODO
        ...

    def speak(self) -> str:
        # TODO
        ...

    def describe(self) -> str:
        # TODO (use self.speak())
        ...


class Dog(Animal):
    # TODO
    ...


class Cat(Animal):
    # TODO
    ...


# 8. super(). Employee extends Person with a salary. Person.describe() -> "Sara (30)";
#    Employee.describe() -> "Sara (30), salary 5000" (reuse the parent's describe).
class Person:
    def __init__(self, name: str, age: int):
        # TODO
        ...

    def describe(self) -> str:
        # TODO
        ...


class Employee(Person):
    def __init__(self, name: str, age: int, salary: int):
        # TODO (call super().__init__)
        ...

    def describe(self) -> str:
        # TODO
        ...


# 9. Money in cents. from_string("12.50 EGP") builds Money(1250, "EGP"); str() gives "12.50 EGP";
#    adding two Money values of the same currency adds them (different currencies raise ValueError);
#    is_valid_currency("EGP") is a static method: three letters.
class Money:
    def __init__(self, cents: int, currency: str):
        # TODO
        ...

    @classmethod
    def from_string(cls, text: str) -> "Money":
        # TODO
        ...

    @staticmethod
    def is_valid_currency(code: str) -> bool:
        # TODO
        ...

    def __str__(self) -> str:
        # TODO
        ...

    def __add__(self, other: "Money") -> "Money":
        # TODO
        ...

    def __eq__(self, other):
        # TODO
        ...


# 10. Class attribute. Each Ticket gets the next id (1, 2, 3...). Ticket.count is how many exist.
class Ticket:
    count = 0

    def __init__(self):
        # TODO
        ...


# 11. A dataclass. Member("Ali") has shares=1 and its own empty tags list (not shared between members).
@dataclass
class Member:
    name: str
    # TODO: shares (default 1) and tags (a list, default empty, one per instance)


# 12. A mixin. Any class that uses JsonMixin gets to_json(): its attributes as JSON with sorted keys.
class JsonMixin:
    def to_json(self) -> str:
        # TODO (vars(self), json.dumps)
        ...


class User(JsonMixin):
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role


# 13. Cooperative super() in a diamond. Each who() returns its own letter followed by whatever
#     comes next in the MRO: D().who() == ["D", "B", "C", "A"]
class A:
    def who(self) -> list:
        # TODO
        ...


class B(A):
    def who(self) -> list:
        # TODO
        ...


class C(A):
    def who(self) -> list:
        # TODO
        ...


class D(B, C):
    def who(self) -> list:
        # TODO
        ...


if __name__ == "__main__":
    p, q = Point(0, 0), Point(3, 4)
    assert repr(Point(1, 2)) == "Point(1, 2)"
    assert Point(1, 2) == Point(1, 2) and Point(1, 2) != Point(2, 1)
    assert Point(1, 2) != "not a point"
    assert len({Point(1, 2), Point(1, 2), Point(2, 1)}) == 2
    assert p.distance_to(q) == 5.0

    acct = BankAccount(10)
    acct.deposit(5)
    acct.withdraw(3)
    assert acct.balance == 12
    for bad in (lambda: acct.deposit(0), lambda: acct.withdraw(-1), lambda: acct.withdraw(100)):
        try:
            bad()
        except ValueError:
            pass
        else:
            raise AssertionError("expected ValueError")
    try:
        acct.balance = 5  # a read-only property cannot be set
    except AttributeError:
        pass
    else:
        raise AssertionError("balance must be read-only")

    t = Temperature(100)
    assert t.fahrenheit == 212
    t.fahrenheit = 32
    assert t.celsius == 0

    v = Vector(1, 2) + Vector(3, 4)
    assert v == Vector(4, 6) and Vector(1, 2) * 3 == Vector(3, 6)
    assert abs(Vector(3, 4)) == 5.0
    assert bool(Vector(0, 0)) is False and bool(Vector(0, 1)) is True

    s = Stack()
    assert not s and len(s) == 0
    s.push(1)
    s.push(2)
    assert s and len(s) == 2 and s.peek() == 2 and s.pop() == 2 and s.pop() == 1
    for bad in (s.pop, s.peek):
        try:
            bad()
        except IndexError as e:
            assert str(e) == "empty stack"
        else:
            raise AssertionError("expected IndexError")

    pl = Playlist("a", "b", "c")
    assert len(pl) == 3 and pl[0] == "a" and pl[-1] == "c" and "b" in pl and "z" not in pl
    assert list(pl) == ["a", "b", "c"] and pl[1:] == ["b", "c"]

    assert Dog("Rex").describe() == "Rex says Woof"
    assert Cat("Tom").describe() == "Tom says Meow"
    assert Animal("X").describe() == "X says ..."
    assert isinstance(Dog("Rex"), Animal)

    assert Person("Sara", 30).describe() == "Sara (30)"
    e = Employee("Sara", 30, 5000)
    assert e.describe() == "Sara (30), salary 5000"
    assert isinstance(e, Person)

    m = Money.from_string("12.50 EGP")
    assert m == Money(1250, "EGP") and str(m) == "12.50 EGP"
    assert str(m + Money(50, "EGP")) == "13.00 EGP"
    try:
        m + Money(1, "USD")
    except ValueError:
        pass
    else:
        raise AssertionError("mixed currencies must raise ValueError")
    assert Money.is_valid_currency("EGP") and not Money.is_valid_currency("EG")

    Ticket.count = 0
    first, second = Ticket(), Ticket()
    assert (first.id, second.id) == (1, 2) and Ticket.count == 2

    a, b = Member("Ali"), Member("Sara", 2)
    assert a.shares == 1 and b.shares == 2 and a == Member("Ali")
    a.tags.append("family")
    assert b.tags == [] and Member("Omar").tags == [], "tags must not be shared"

    assert json.loads(User("Ali", "admin").to_json()) == {"name": "Ali", "role": "admin"}
    assert User("Ali", "admin").to_json() == '{"name": "Ali", "role": "admin"}'

    assert D().who() == ["D", "B", "C", "A"]
    assert [c.__name__ for c in D.__mro__] == ["D", "B", "C", "A", "object"]
    print("All checks passed")
