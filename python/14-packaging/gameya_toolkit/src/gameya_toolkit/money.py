"""Money helpers. This module is finished; you package it."""


def format_money(cents: int, currency: str = "EGP") -> str:
    """Format piasters for people: 125050 -> '1,250.50 EGP'."""
    if cents < 0:
        raise ValueError("cents cannot be negative")
    return f"{cents // 100:,}.{cents % 100:02d} {currency}"
