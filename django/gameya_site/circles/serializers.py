"""Serializers: turn Gameya and Member rows into JSON, and check JSON coming in. Module 06."""

from rest_framework import serializers  # noqa: F401  (you will use it)

from .models import Gameya, Member  # noqa: F401

# TODO 16: class GameyaSerializer(serializers.ModelSerializer), with Meta model = Gameya.
#          Fields: id, name, start_date, weeks, per_week, share_value, turns, payout, weekly_pot.
#          turns, payout and weekly_pot are model properties. Listing them in fields is enough:
#          DRF reads them and makes them read-only. weeks and share_value must be at least 1.
#          per_week is optional and must be at least 1. Without these rules, 0 can reach the
#          database.
# TODO 17: class MemberSerializer(serializers.ModelSerializer), with Meta model = Member.
#          Fields: id, gameya, name, shares, due. due is a method with no arguments, so listing
#          it in fields is enough and it stays read-only. shares is optional and must
#          be at least 1. Keep both gameya and name in fields, so DRF can check the
#          (gameya, name) constraint and return a 400 for a duplicate.
