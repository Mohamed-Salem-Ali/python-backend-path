"""Reusable queries over the models. Module 02, second half.

Each function has a precise contract and a test in circles/tests/test_queries.py. Where the
docstring says "one query", the test counts queries, so lazy QuerySets, annotate and
select_related matter. Do the work in the database, not in Python loops, unless told otherwise.
"""

from datetime import date  # noqa: F401  (used in the signatures)

from django.db.models import QuerySet  # noqa: F401

from .models import Gameya, Member, Payment  # noqa: F401


def unpaid_members(gameya: Gameya, week: int, today: date) -> QuerySet[Member]:
    """Members of the gameya with no payment for `week`, but only once that week has started
    (its payout day is on or before `today`). Before it starts nobody is unpaid: return an empty
    QuerySet. Return a QuerySet (not a list), ordered like Member's default ordering."""
    # TODO (exclude(payments__week=week), Member.objects.none())
    ...


def total_collected(gameya: Gameya) -> int:
    """Total of every payment amount in the gameya; 0 when there are none. One query."""
    # TODO (aggregate with Sum, and Coalesce or `or 0`)
    ...


def member_totals(gameya: Gameya) -> QuerySet[Member]:
    """The gameya's members, each annotated with `paid_total` (sum of their payment amounts, 0 if
    none) and `paid_weeks` (how many payments). Order by highest paid_total, then name.
    Evaluating it must take exactly one query."""
    # TODO (annotate with Sum/Count and Coalesce, order_by)
    ...


def weekly_summary(gameya: Gameya) -> list[dict]:
    """For every week that has payments, in week order:
    [{"week": 1, "count": 2, "amount": 300}, ...]. One query."""
    # TODO (values("week").annotate(...).order_by("week"))
    ...


def members_with_turns(gameya: Gameya) -> QuerySet[Member]:
    """Only members holding at least one payout slot, annotated with `turn_count`. Order by most
    turns first, then name. Evaluating it must take exactly one query."""
    # TODO
    ...


def weeks_owed(member: Member, today: date) -> list[int]:
    """The week numbers that have started (payout day on or before `today`) and that the member
    has not paid, in ascending order. Never include weeks beyond the gameya's last week."""
    # TODO
    ...


def advance_payments(gameya: Gameya) -> list[Payment]:
    """Payments made before their week's payment window opened, each with its member loaded.
    Looping over the result and reading payment.member.name must not cause extra queries:
    the whole thing takes exactly one query."""
    # TODO (select_related, then filter in Python using Payment.is_advance)
    ...
