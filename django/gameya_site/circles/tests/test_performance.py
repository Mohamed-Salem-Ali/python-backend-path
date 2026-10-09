"""Module 09 acceptance tests: query counts, the summary cache and its invalidation. Do not edit.

Run (from django/gameya_site):  pytest circles/tests/test_performance.py

They need circles/caching.py (TODO 31 to 33), the receivers in circles/signals.py (TODO 33) and
the CACHES setting (TODO 34). They also use the models, factories and fixtures of modules 02 to 08.
"""

import time

import pytest
from django.core.cache import cache

from circles.caching import build_summary, gameya_summary, invalidate_summary
from circles.models import Gameya, Payment
from circles.tests import factories as circle_factories


@pytest.fixture(autouse=True)
def empty_cache():
    # The cache lives in memory and every test shares it, so each test starts with it empty.
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def circle(db):
    # Ali has one share, so pays 500 a week, and has paid weeks 1 and 2: 1000 in all. Sara has two
    # shares, so pays 1000 a week, and has paid 600 in week 1. Collected in total: 1600.
    gameya = circle_factories.GameyaFactory(share_value=500)
    ali = circle_factories.MemberFactory(gameya=gameya, name="Ali", shares=1)
    sara = circle_factories.MemberFactory(gameya=gameya, name="Sara", shares=2)
    circle_factories.PaymentFactory(member=ali, week=1, amount=500)
    circle_factories.PaymentFactory(member=ali, week=2, amount=500)
    circle_factories.PaymentFactory(member=sara, week=1, amount=600)
    return gameya


# Building the summary: the numbers, and a fixed number of queries.


def test_build_summary_gives_each_members_due_and_paid_total(circle):
    summary = build_summary(circle.pk)
    assert summary["name"] == circle.name
    assert summary["collected"] == 1600
    assert summary["members"] == [
        {"name": "Ali", "due": 500, "paid": 1000},
        {"name": "Sara", "due": 1000, "paid": 600},
    ]


def test_build_summary_of_a_gameya_with_no_members(db):
    gameya = circle_factories.GameyaFactory()
    assert build_summary(gameya.pk) == {"name": gameya.name, "collected": 0, "members": []}


def test_a_member_with_no_payments_has_zero_paid(db):
    gameya = circle_factories.GameyaFactory(share_value=500)
    circle_factories.MemberFactory(gameya=gameya, name="Omar", shares=1)
    assert build_summary(gameya.pk)["members"] == [{"name": "Omar", "due": 500, "paid": 0}]


@pytest.mark.parametrize("member_count", [1, 10], ids=["one member", "ten members"])
def test_build_summary_runs_at_most_three_queries(member_count, db, django_assert_max_num_queries):
    gameya = circle_factories.GameyaFactory()
    for _ in range(member_count):
        circle_factories.PaymentFactory(member=circle_factories.MemberFactory(gameya=gameya))
    with django_assert_max_num_queries(3):
        summary = build_summary(gameya.pk)
    assert len(summary["members"]) == member_count


def test_build_summary_raises_for_a_missing_gameya(db):
    with pytest.raises(Gameya.DoesNotExist):
        build_summary(999999)


# The cache: a second call does no work, and a change clears the entry.


def test_the_second_call_is_served_from_the_cache(circle, django_assert_num_queries):
    gameya_summary(circle.pk)
    with django_assert_num_queries(0):
        summary = gameya_summary(circle.pk)
    assert summary["collected"] == 1600


def test_the_summary_is_stored_under_its_key(circle):
    gameya_summary(circle.pk)
    assert cache.get(f"gameya:{circle.pk}:summary")["collected"] == 1600


def test_a_new_payment_clears_the_cached_summary(circle):
    assert gameya_summary(circle.pk)["collected"] == 1600
    ali = circle.members.get(name="Ali")
    circle_factories.PaymentFactory(member=ali, week=3, amount=500)
    assert gameya_summary(circle.pk)["collected"] == 2100


def test_a_changed_payment_clears_the_cached_summary(circle):
    assert gameya_summary(circle.pk)["collected"] == 1600
    payment = Payment.objects.get(member__name="Sara", week=1)
    payment.amount = 800
    payment.save()
    assert gameya_summary(circle.pk)["collected"] == 1800


def test_a_deleted_payment_clears_the_cached_summary(circle):
    assert gameya_summary(circle.pk)["collected"] == 1600
    Payment.objects.get(member__name="Ali", week=1).delete()
    assert gameya_summary(circle.pk)["collected"] == 1100


def test_a_payment_clears_only_its_own_gameyas_summary(db, django_assert_num_queries):
    # The member is given the id of the first gameya, on any database. A receiver that uses the
    # member's id in place of the gameya's id would clear the wrong entry, and this test catches it.
    first = circle_factories.GameyaFactory()
    second = circle_factories.GameyaFactory()
    member = circle_factories.MemberFactory(pk=first.pk, gameya=second)
    gameya_summary(first.pk)
    gameya_summary(second.pk)
    circle_factories.PaymentFactory(member=member)
    with django_assert_num_queries(0):
        gameya_summary(first.pk)
    assert gameya_summary(second.pk)["collected"] == 500


def test_a_new_member_clears_the_cached_summary(circle):
    assert len(gameya_summary(circle.pk)["members"]) == 2
    circle_factories.MemberFactory(gameya=circle, name="Omar")
    assert len(gameya_summary(circle.pk)["members"]) == 3


def test_a_deleted_member_with_no_payments_clears_the_cached_summary(circle):
    # Omar has no payments, so deleting him cascades to nothing: only his own signal can clear it.
    omar = circle_factories.MemberFactory(gameya=circle, name="Omar")
    assert len(gameya_summary(circle.pk)["members"]) == 3
    omar.delete()
    assert len(gameya_summary(circle.pk)["members"]) == 2


def test_a_change_in_one_gameya_keeps_the_summary_of_another(circle, django_assert_num_queries):
    other = circle_factories.GameyaFactory()
    gameya_summary(circle.pk)
    circle_factories.PaymentFactory(member=circle_factories.MemberFactory(gameya=other))
    with django_assert_num_queries(0):
        summary = gameya_summary(circle.pk)
    assert summary["collected"] == 1600


def test_invalidate_summary_removes_the_entry(circle):
    gameya_summary(circle.pk)
    assert cache.get(f"gameya:{circle.pk}:summary") is not None
    invalidate_summary(circle.pk)
    assert cache.get(f"gameya:{circle.pk}:summary") is None


# Settings: the default cache keeps an entry for five minutes.


def test_the_default_cache_keeps_entries_for_five_minutes(settings):
    assert settings.CACHES["default"]["TIMEOUT"] == 300


def test_a_cached_summary_expires_after_the_default_timeout(circle, monkeypatch):
    # A fake clock: the cache reads time.time(), so each step moves the clock forward.
    now = [1_000_000.0]
    monkeypatch.setattr(time, "time", lambda: now[0])
    key = f"gameya:{circle.pk}:summary"
    gameya_summary(circle.pk)
    now[0] += 299
    assert cache.get(key) is not None
    now[0] += 2
    assert cache.get(key) is None
