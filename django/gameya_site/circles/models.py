"""The data model. Module 02.

Four models describe a rotating savings circle:

    Gameya  1 ---- *  Member  1 ---- *  Payment
       |
       1 ---- *  PayoutSlot  * ---- 0..1  Member   (who collects that turn, once assigned)

Build them one at a time. After each, run:

    python manage.py makemigrations
    python manage.py migrate
    python manage.py test circles.tests.test_models

The tests in circles/tests/test_models.py are the full specification.
"""

from datetime import date, timedelta  # noqa: F401  (you will need these)

from django.core.exceptions import ValidationError  # noqa: F401
from django.db import models


class Gameya(models.Model):
    """One savings circle.

    Fields:
      name         text, up to 80 characters
      start_date   date of week 1's payout day
      weeks        how many weeks it runs (whole number, at least 1)
      per_week     payouts each week (whole number, at least 1, default 1)
      share_value  what one name pays each week (whole number, at least 1)
      created_at   set automatically when the row is created

    Meta: order by name. Database constraints (CheckConstraint, with the names the tests expect):
      gameya_weeks_positive, gameya_per_week_positive, gameya_share_value_positive

    Also: __str__ returns the name; properties turns, payout and weekly_pot (same rules as the
    Python weeks); methods week_start(week) and pay_window_start(week) returning dates.
    """

    # TODO


class Member(models.Model):
    """A person in a gameya, with one or more names (shares).

    Fields: gameya (ForeignKey, related_name="members", delete with the gameya), name (80),
            shares (whole number, default 1), created_at (automatic).
    Meta: order by id. A UniqueConstraint named "member_name_unique_per_gameya" on (gameya, name).
    __str__: "Ali (Alf)" (member name, then the gameya name).
    Methods: due() what they pay each week (shares * the gameya's share_value);
             status(week, today) -> "paid", "advance", "unpaid" or "upcoming".
    """

    # TODO


class Payment(models.Model):
    """A member's payment for one week.

    Fields: member (ForeignKey, related_name="payments"), week (whole number), paid_on (date),
            amount (whole number).
    Meta: order by week then id. A UniqueConstraint "one_payment_per_member_week" on (member, week).
    __str__: "Ali: week 1".
    clean(): raise ValidationError unless 1 <= week <= the gameya's weeks.
    Property is_advance: True when paid_on is before the gameya's pay_window_start(week).
    """

    # TODO


class PayoutSlot(models.Model):
    """One payout turn. A member is assigned later, so member can be empty.

    Fields: gameya (ForeignKey, related_name="slots"), turn_number (whole number),
            member (ForeignKey to Member, related_name="slots", optional, set to NULL when the
            member is deleted), delivered_at (optional date and time).
    Meta: order by turn_number. A UniqueConstraint "one_slot_per_turn" on (gameya, turn_number).
    __str__: "Turn 3 (week 2)". Property week: the week this turn falls in, from per_week.
    """

    # TODO
