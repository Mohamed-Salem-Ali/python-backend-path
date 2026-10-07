"""Week 3 project: the Gameya domain model as classes. See README.md."""

from collections.abc import Iterator
from dataclasses import dataclass
from datetime import date, timedelta
from functools import wraps


class InvalidSetup(ValueError):
    """The gameya numbers or start date are not valid."""


class DuplicateMember(ValueError):
    """A member with that name already exists."""


class TurnLimitExceeded(ValueError):
    """A member cannot hold more turns than they have shares."""


@dataclass(frozen=True)
class Setup:
    weeks: int
    per_week: int
    share_value: int
    start: str  # ISO date of week 1's payout day

    def __post_init__(self) -> None:
        # TODO: weeks, per_week and share_value must be positive ints (not bool);
        #       start must be a valid ISO date. Otherwise raise InvalidSetup.
        ...

    @property
    def turns(self) -> int:
        # TODO
        ...

    @property
    def payout(self) -> int:
        # TODO
        ...

    @property
    def weekly_pot(self) -> int:
        # TODO
        ...


@dataclass
class Member:
    name: str
    shares: int = 1

    def due(self, share_value: int) -> int:
        """What this member pays each week."""
        # TODO
        ...


def audited(method):
    """Decorator for Gameya methods. After a successful call, append 'method_name: args' to
    self.audit_log. If the method raises, log nothing. Keep the method's name and docstring."""
    # TODO
    return method


class Gameya:
    def __init__(self, name: str, setup: Setup):
        self.name = name
        self.setup = setup
        self.audit_log: list = []
        # TODO: members by name, payments as {(name, week): paid_on}, turns as {turn_number: name}
        ...

    # ---- members ----
    @audited
    def add_member(self, name: str, shares: int = 1) -> Member:
        """Add a member; raise DuplicateMember if the name exists, ValueError if shares < 1."""
        # TODO
        ...

    def __len__(self) -> int:
        # TODO: number of members
        ...

    def __contains__(self, name: str) -> bool:
        # TODO
        ...

    def __iter__(self) -> Iterator[Member]:
        # TODO: iterate over the members in the order they were added
        ...

    @property
    def total_shares(self) -> int:
        # TODO
        ...

    # ---- payments ----
    @audited
    def record_payment(self, name: str, week: int, paid_on: str) -> None:
        """Record that `name` paid for `week` on the ISO date `paid_on`.
        Unknown member: KeyError. Week outside 1..weeks: ValueError."""
        # TODO
        ...

    def week_start(self, week: int) -> str:
        """ISO payout day of `week`."""
        # TODO
        ...

    def pay_window_start(self, week: int) -> str:
        """ISO date the payment window opens: the Sunday on or before the payout day."""
        # TODO
        ...

    def status(self, name: str, week: int, today: str) -> str:
        """'paid', 'advance', 'unpaid' or 'upcoming' (same rules as the week 2 project)."""
        # TODO
        ...

    # ---- turns ----
    def slots(self) -> Iterator[tuple[int, int]]:
        """Lazily yield (turn_number, week) for every turn: with per_week=2, turn 1 and 2 are
        week 1, turns 3 and 4 are week 2, and so on."""
        # TODO (a generator)
        ...

    @audited
    def assign(self, turn_number: int, name: str) -> None:
        """Give a turn to a member. ValueError for a turn outside 1..turns or one already taken;
        KeyError for an unknown member; TurnLimitExceeded if they already hold as many turns as
        they have shares."""
        # TODO
        ...

    def turns_of(self, name: str) -> list:
        """The member's turn numbers, ascending."""
        # TODO
        ...

    def holder(self, turn_number: int) -> str | None:
        """Who holds the turn, or None if nobody does yet."""
        # TODO
        ...


if __name__ == "__main__":
    # Setup: validation and derived figures
    s = Setup(weeks=10, per_week=2, share_value=100, start="2026-10-10")
    assert (s.turns, s.payout, s.weekly_pot) == (20, 1000, 2000)
    for bad in (
        dict(weeks=0, per_week=2, share_value=100, start="2026-10-10"),
        dict(weeks=10, per_week=2, share_value=1.5, start="2026-10-10"),
        dict(weeks=10, per_week=True, share_value=100, start="2026-10-10"),
        dict(weeks=10, per_week=2, share_value=100, start="10/10/2026"),
        dict(weeks=10, per_week=2, share_value=100, start="2026-13-40"),
    ):
        try:
            Setup(**bad)
        except InvalidSetup:
            pass
        else:
            raise AssertionError(f"{bad} should be invalid")
    try:
        s.weeks = 5  # frozen
    except AttributeError:
        pass
    else:
        raise AssertionError("Setup must be frozen")

    # Members
    assert Member("Ali").shares == 1 and Member("Sara", 2).due(100) == 200
    g = Gameya("Alf", Setup(weeks=3, per_week=2, share_value=100, start="2026-10-10"))
    assert len(g) == 0
    g.add_member("Ali", 2)
    g.add_member("Sara")
    assert len(g) == 2 and "Ali" in g and "Omar" not in g and g.total_shares == 3
    assert [m.name for m in g] == ["Ali", "Sara"]
    for bad_call, error in (
        (lambda: g.add_member("Ali"), DuplicateMember),
        (lambda: g.add_member("Zed", 0), ValueError),
    ):
        try:
            bad_call()
        except error:
            pass
        else:
            raise AssertionError(f"expected {error.__name__}")
    assert len(g) == 2

    # Dates and statuses
    assert g.week_start(1) == "2026-10-10" and g.week_start(3) == "2026-10-24"
    assert g.pay_window_start(1) == "2026-10-04" and g.pay_window_start(2) == "2026-10-11"
    assert g.status("Ali", 1, today="2026-10-05") == "upcoming"
    assert g.status("Ali", 1, today="2026-10-12") == "unpaid"
    g.record_payment("Ali", 1, "2026-10-05")  # inside the window
    g.record_payment("Ali", 2, "2026-10-04")  # before week 2's window opens
    assert g.status("Ali", 1, today="2026-10-12") == "paid"
    assert g.status("Ali", 2, today="2026-10-12") == "advance"
    assert g.status("Sara", 1, today="2026-10-12") == "unpaid"
    for bad_call, error in (
        (lambda: g.record_payment("Nobody", 1, "2026-10-05"), KeyError),
        (lambda: g.record_payment("Ali", 4, "2026-10-05"), ValueError),
    ):
        try:
            bad_call()
        except error:
            pass
        else:
            raise AssertionError(f"expected {error.__name__}")

    # Turns: lazy slots and the per-name limit
    assert list(g.slots()) == [(1, 1), (2, 1), (3, 2), (4, 2), (5, 3), (6, 3)]
    assert hasattr(g.slots(), "__next__"), "slots must be a generator"
    g.assign(1, "Ali")
    g.assign(3, "Ali")  # Ali has 2 shares
    g.assign(2, "Sara")
    assert g.turns_of("Ali") == [1, 3] and g.holder(1) == "Ali" and g.holder(4) is None
    for bad_call, error in (
        (lambda: g.assign(5, "Ali"), TurnLimitExceeded),  # a third turn for 2 shares
        (lambda: g.assign(2, "Ali"), ValueError),  # already taken
        (lambda: g.assign(7, "Sara"), ValueError),  # outside 1..6
        (lambda: g.assign(4, "Nobody"), KeyError),
        (lambda: g.assign(4, "Sara"), TurnLimitExceeded),  # Sara has 1 share and holds turn 2
    ):
        try:
            bad_call()
        except error:
            pass
        else:
            raise AssertionError(f"expected {error.__name__}")

    # The audit decorator logs only successful calls and keeps metadata
    names = [entry.split(":")[0] for entry in g.audit_log]
    assert names == [
        "add_member",
        "add_member",
        "record_payment",
        "record_payment",
        "assign",
        "assign",
        "assign",
    ], names
    assert Gameya.add_member.__name__ == "add_member" and Gameya.add_member.__doc__
    print("All checks passed")
