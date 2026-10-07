"""Your tests for payments.py. Replace every placeholder line (the ones that say NotImplementedError) with a real test.

Run them:        pytest python/13-testing/test_payments.py
Then check them: python python/13-testing/check_tests.py
(the checker runs your tests against broken copies of payments.py; good tests catch every bug)
"""

from unittest.mock import Mock

import pytest
from payments import Ledger, convert, load_ledger, parse_amount, today_label


# A fixture gives each test a fresh object. Build a ledger with three entries from two members,
# for example Ali 100.00 EGP twice and Sara 50.00 EGP once (amounts are in piasters).
@pytest.fixture
def ledger() -> Ledger:
    raise NotImplementedError("TODO: build and return a Ledger with entries from two members")


# 1. Parametrize: several valid texts and the piasters they should give.
#    Include a thousands separator ("1,250.50"), a whole number, and surrounding spaces.
def test_parse_amount_valid():
    raise NotImplementedError(
        "TODO: @pytest.mark.parametrize, then assert parse_amount(text) == cents"
    )


# 2. Parametrize: texts that must raise ValueError (not a number, empty, zero, negative,
#    three decimals). Use pytest.raises.
def test_parse_amount_invalid():
    raise NotImplementedError("TODO: @pytest.mark.parametrize with pytest.raises(ValueError)")


# 3. The total of the fixture ledger, and the length. Use the `ledger` fixture as an argument.
def test_ledger_total():
    raise NotImplementedError("TODO")


# 4. add() rejects zero and negative amounts with ValueError, and a rejected entry is not stored.
def test_ledger_rejects_non_positive():
    raise NotImplementedError("TODO: pytest.raises(ValueError, match=...)")


# 5. balance_of() counts only that member's entries (and is 0 for an unknown member).
def test_balance_is_per_member():
    raise NotImplementedError("TODO")


# 6. convert() rounds to the nearest minor unit. Pass a plain function as fetch_rate
#    (for example `lambda currency: 0.0319`). Pick numbers where rounding and truncating differ.
def test_convert_rounds():
    raise NotImplementedError("TODO")


# 7. convert() asks for the rate exactly once, with the right currency. Use unittest.mock.Mock
#    (Mock(return_value=...)) and assert on how it was called. Also: a negative amount raises.
def test_convert_fetches_rate_once():
    raise NotImplementedError("TODO: Mock, assert_called_once_with")


# 8. load_ledger() reads a JSON file. Use the tmp_path fixture to write one, then load it.
def test_load_ledger(tmp_path):
    raise NotImplementedError("TODO: tmp_path / 'ledger.json', write_text, load_ledger")


# 9. A missing file raises FileNotFoundError (do not swallow it).
def test_load_ledger_missing_file(tmp_path):
    raise NotImplementedError("TODO")


# 10. today_label() formats the date as 'Saturday 10 October 2026'. Use monkeypatch to replace
#     payments._today with a function that returns a fixed date, so the test never depends on today.
def test_today_label(monkeypatch):
    raise NotImplementedError("TODO: monkeypatch.setattr(payments, '_today', ...)")
