"""Factories: build test data with one call. Module 08.

A factory describes how to make a valid object, with defaults you can override in each test.
"""

from datetime import date  # noqa: F401  (you will use it)

import factory  # noqa: F401  (you will use it)

from circles.models import Gameya, Member, Payment  # noqa: F401

# TODO 29: three factories. Each one is a subclass of factory.django.DjangoModelFactory, with a
#          class Meta that names its model (Gameya, Member or Payment).
#   GameyaFactory: name is a sequence, so each gameya gets a new name that starts with "Gameya "
#                  (for example "Gameya 0", then "Gameya 1"). start_date is 2026-10-11, weeks is
#                  10, per_week is 1, and share_value is 500.
#   MemberFactory: gameya is a sub-factory that builds a gameya with GameyaFactory, unless the
#                  test passes one. name is a sequence that starts with "Member ". shares is 1.
#   PaymentFactory: member is a sub-factory that builds a member with MemberFactory. week is 1,
#                  and paid_on is 2026-10-11. amount is computed from the member: it is what the
#                  member owes for one week, the value of the member's due() method.
#
# Do not import a name before it is defined here: a failed import breaks every test that uses
# this module. Once the three classes exist, the imports above can stay as they are.
