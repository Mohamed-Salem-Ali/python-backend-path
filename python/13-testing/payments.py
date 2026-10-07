"""Small payment helpers for practising tests (Module 13). This is the code under test:
read it, but do not change it. You write the tests in test_payments.py."""

import json
from collections.abc import Callable
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path


def parse_amount(text: str) -> int:
    """Turn '1,250.50' into 125050 (piasters). Raise ValueError unless it is a positive amount
    with at most two decimals."""
    cleaned = text.strip().replace(",", "")
    try:
        amount = Decimal(cleaned)
    except InvalidOperation:
        raise ValueError(f"not an amount: {text!r}") from None
    if amount <= 0:
        raise ValueError("amount must be positive")
    if amount.as_tuple().exponent < -2:
        raise ValueError("at most two decimals")
    return int(amount * 100)


class Ledger:
    """Payments received, as (member, piasters) entries."""

    def __init__(self) -> None:
        self._entries: list[tuple[str, int]] = []

    def add(self, member: str, cents: int) -> None:
        if cents <= 0:
            raise ValueError("amount must be positive")
        self._entries.append((member, cents))

    def total(self) -> int:
        return sum(c for _, c in self._entries)

    def balance_of(self, member: str) -> int:
        return sum(c for m, c in self._entries if m == member)

    def members(self) -> list[str]:
        return sorted({m for m, _ in self._entries})

    def __len__(self) -> int:
        return len(self._entries)


def convert(cents: int, currency: str, fetch_rate: Callable[[str], float]) -> int:
    """Convert piasters into the minor units of `currency`. `fetch_rate(currency)` returns
    how many units of that currency one piaster is worth (it may call a network service)."""
    if cents < 0:
        raise ValueError("cents cannot be negative")
    rate = fetch_rate(currency)
    return round(cents * rate)


def load_ledger(path: Path) -> Ledger:
    """Read {"entries": [["Ali", 10000], ...]} from a JSON file into a Ledger."""
    data = json.loads(path.read_text(encoding="utf-8"))
    ledger = Ledger()
    for member, cents in data["entries"]:
        ledger.add(member, cents)
    return ledger


def _today() -> date:
    return date.today()


def today_label() -> str:
    """For example 'Saturday 10 October 2026'."""
    return _today().strftime("%A %d %B %Y")
