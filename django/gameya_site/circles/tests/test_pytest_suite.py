"""Module 08 acceptance tests: pytest and pytest-django, with factories and fixtures. Do not edit.

Run (from django/gameya_site):  pytest circles/tests/test_pytest_suite.py

These tests use pytest's plain functions, not Django's TestCase classes, so run them with pytest.
They need pytest, pytest-django and factory-boy installed, the pytest.ini file (TODO 28), the
factories (TODO 29) and the fixtures in conftest.py (TODO 30). They also use the code of
modules 02 to 07: the models, the gameya page, the admin and the API.
"""

import pytest
from django.urls import reverse

from circles.models import Gameya, Member
from circles.tests import factories as circle_factories

# Unsaved objects need no database, so the tests below do not ask for db.


@pytest.mark.parametrize(
    "shares, expected_due",
    [(1, 500), (2, 1000), (3, 1500)],
    ids=["one share", "two shares", "three shares"],
)
def test_due_is_shares_times_the_share_value(shares, expected_due):
    member = Member(name="Ali", shares=shares, gameya=Gameya(share_value=500))
    assert member.due() == expected_due


@pytest.mark.parametrize(
    "weeks, per_week, share_value, turns, payout, weekly_pot",
    [
        (10, 1, 500, 10, 5000, 5000),
        (8, 2, 200, 16, 1600, 3200),
        (12, 3, 100, 36, 1200, 3600),
    ],
    ids=["one payout a week", "two payouts a week", "three payouts a week"],
)
def test_the_gameya_figures(weeks, per_week, share_value, turns, payout, weekly_pot):
    gameya = Gameya(weeks=weeks, per_week=per_week, share_value=share_value)
    assert (gameya.turns, gameya.payout, gameya.weekly_pot) == (turns, payout, weekly_pot)


# Factories: the test data builders from TODO 29.


def test_the_gameya_factory_has_the_default_values(db):
    gameya = circle_factories.GameyaFactory()
    assert (gameya.weeks, gameya.per_week, gameya.share_value) == (10, 1, 500)
    assert str(gameya.start_date) == "2026-10-11"


def test_each_gameya_from_the_factory_gets_its_own_name(db):
    first = circle_factories.GameyaFactory()
    second = circle_factories.GameyaFactory()
    assert first.name != second.name
    assert first.name.startswith("Gameya ")


def test_a_member_from_the_factory_gets_a_new_gameya_by_default(db):
    member = circle_factories.MemberFactory()
    assert Gameya.objects.count() == 1
    assert member.gameya == Gameya.objects.get()
    assert member.shares == 1


def test_each_member_from_the_factory_gets_its_own_gameya(db):
    first = circle_factories.MemberFactory()
    second = circle_factories.MemberFactory()
    assert first.gameya != second.gameya
    assert Gameya.objects.count() == 2


def test_a_member_from_the_factory_can_use_a_gameya_it_is_given(db, gameya):
    member = circle_factories.MemberFactory(gameya=gameya)
    assert member.gameya == gameya
    assert Gameya.objects.count() == 1


def test_a_payment_from_the_factory_defaults_to_its_members_weekly_due(db):
    # member__shares reaches into the SubFactory: the member gets two shares.
    payment = circle_factories.PaymentFactory(member__shares=2)
    assert payment.amount == 1000
    assert payment.week == 1
    assert str(payment.paid_on) == "2026-10-11"


def test_create_batch_makes_several_members_in_one_gameya(db, gameya):
    circle_factories.MemberFactory.create_batch(3, gameya=gameya)
    assert gameya.members.count() == 3


# Fixtures: the shared setup from TODO 30 in conftest.py.


def test_the_gameya_fixture_is_saved(gameya):
    assert Gameya.objects.filter(pk=gameya.pk).exists()


def test_the_staff_token_belongs_to_a_staff_user(staff_token):
    assert staff_token.user.is_staff is True


def test_the_reader_token_belongs_to_a_user_who_is_not_staff(reader_token):
    assert reader_token.user.is_staff is False


def test_the_staff_client_can_open_the_admin(staff_client):
    response = staff_client.get(reverse("admin:circles_gameya_changelist"))
    assert response.status_code == 200


def test_the_api_client_starts_without_a_login(api_client):
    response = api_client.post(
        reverse("gameya-list"),
        {"name": "X", "start_date": "2026-11-01", "weeks": 2, "share_value": 10},
    )
    assert response.status_code == 401


# Parametrize the API: one test, one case per kind of user.


@pytest.mark.parametrize(
    "who, expected_status",
    [("anonymous", 401), ("reader", 403), ("staff", 201)],
    ids=["anonymous", "logged in, not staff", "staff"],
)
def test_who_may_create_a_gameya(who, expected_status, api_client, request, db):
    if who != "anonymous":
        token = request.getfixturevalue(f"{who}_token")
        api_client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    response = api_client.post(
        reverse("gameya-list"),
        {"name": "New", "start_date": "2026-11-01", "weeks": 4, "share_value": 250},
    )
    assert response.status_code == expected_status


@pytest.mark.parametrize("field", ["weeks", "per_week", "share_value"])
def test_zero_is_rejected_for_each_gameya_number(field, api_client, staff_token, db):
    api_client.credentials(HTTP_AUTHORIZATION=f"Token {staff_token.key}")
    data = {"name": "Zero", "start_date": "2026-11-01", "weeks": 4, "share_value": 250}
    data[field] = 0
    response = api_client.post(reverse("gameya-list"), data)
    assert response.status_code == 400
    assert field in response.json()


# pytest-django's own fixtures: query counts and settings.


def test_the_gameya_page_runs_two_queries_however_many_members(
    client, django_assert_num_queries, gameya
):
    circle_factories.MemberFactory.create_batch(5, gameya=gameya)
    with django_assert_num_queries(2):
        response = client.get(reverse("gameya_page", args=[gameya.pk]))
    assert response.status_code == 200
    assert "circles/gameya_detail.html" in [t.name for t in response.templates]


def test_the_settings_fixture_changes_the_static_url(client, settings, gameya):
    settings.STATIC_URL = "/assets/"
    response = client.get(reverse("gameya_page", args=[gameya.pk]))
    assert b"/assets/circles/site.css" in response.content
