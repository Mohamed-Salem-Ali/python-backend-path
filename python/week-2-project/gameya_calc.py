"""Week 2 project: the Gameya rules as pure functions plus a small CLI. See README.md."""

import argparse
import json
import sys
from datetime import date, timedelta


class InvalidSetup(ValueError):
    """The gameya numbers are not valid (must be positive whole numbers)."""


def validate_setup(weeks: int, per_week: int, share_value: int) -> None:
    """Raise InvalidSetup if any value is not a positive integer."""
    # TODO
    ...


def turns(weeks: int, per_week: int) -> int:
    # TODO
    ...


def payout(weeks: int, share_value: int) -> int:
    # TODO
    ...


def weekly_pot(weeks: int, per_week: int, share_value: int) -> int:
    # TODO
    ...


def week_start(start: str, week: int) -> str:
    """ISO date of the payout day of `week` (1-based)."""
    # TODO
    ...


def pay_window_start(start: str, week: int) -> str:
    """ISO date the payment window opens: the Sunday on or before the payout day."""
    # TODO
    ...


def status(start: str, week: int, today: str, paid_on: str | None = None) -> str:
    """'paid', 'advance', 'unpaid' or 'upcoming'."""
    # TODO
    ...


def summary(weeks: int, per_week: int, share_value: int, start: str) -> dict:
    """The figures and the week-by-week schedule, validated first."""
    # TODO: return {"turns": ..., "payout": ..., "weekly_pot": ...,
    #               "schedule": [{"week": 1, "payout_day": "...", "window_opens": "..."}, ...]}
    ...


def main(argv: list | None = None) -> int:
    """Command-line entry point. Returns the exit code."""
    # TODO: build an argparse parser (--weeks, --per-week, --share, --start, --json),
    #       print the summary (text or JSON), and handle InvalidSetup (message to stderr, return 2).
    ...


if __name__ == "__main__":
    # Part A checks
    assert turns(10, 2) == 20
    assert payout(10, 100) == 1000
    assert weekly_pot(10, 2, 100) == 2000
    assert week_start("2026-10-10", 1) == "2026-10-10"
    assert week_start("2026-10-10", 3) == "2026-10-24"
    assert pay_window_start("2026-10-10", 1) == "2026-10-04"
    assert pay_window_start("2026-10-10", 2) == "2026-10-11"

    start = "2026-10-10"
    assert status(start, 1, today="2026-10-05") == "upcoming"
    assert status(start, 1, today="2026-10-12") == "unpaid"
    assert status(start, 1, today="2026-10-05", paid_on="2026-10-05") == "paid"
    assert status(start, 1, today="2026-10-12", paid_on="2026-10-04") == "paid"
    assert status(start, 1, today="2026-10-12", paid_on="2026-10-03") == "advance"
    assert status(start, 3, today="2026-10-12", paid_on="2026-10-12") == "advance"

    for bad in ((0, 2, 100), (10, 0, 100), (10, 2, -5), (10, 2, 1.5), (True, 2, 100)):
        try:
            validate_setup(*bad)
        except InvalidSetup:
            pass
        else:
            raise AssertionError(f"{bad} should be invalid")
    validate_setup(10, 2, 100)

    s = summary(3, 1, 50, "2026-10-10")
    assert s["turns"] == 3 and s["payout"] == 150 and s["weekly_pot"] == 150
    assert [row["payout_day"] for row in s["schedule"]] == [
        "2026-10-10",
        "2026-10-17",
        "2026-10-24",
    ]
    assert s["schedule"][1]["window_opens"] == "2026-10-11"
    print("All checks passed")
    # Part B: uncomment when main() is written
    # sys.exit(main())
