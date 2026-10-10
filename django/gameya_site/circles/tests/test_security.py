"""Module 11 acceptance tests: ownership, JWT, CSRF, XSS and production settings. Do not edit.

Run (from django/gameya_site):  pytest circles/tests/test_security.py

They need the Gameya.organiser field (TODO 39), the ownership permission and the move check
(TODO 40 and 41), the JWT routes and settings (TODO 42), the production settings (TODO 43), and
the views, template and API from modules 04 to 06. The last two tests start manage.py in a new
process, with its own environment variables.

Three tests already pass before you start: a non-staff user cannot create a gameya, a staff token
can write without a CSRF token, and the templates keep escaping on. They guard rules from modules
05 and 06 that module 11 must not break, so they pass from the start, on purpose.
"""

import os
import re
import subprocess
import sys
from datetime import timedelta
from pathlib import Path

import pytest
from django.test import Client
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from circles.models import Gameya, Payment
from circles.tests import factories as circle_factories

PASSWORD = "test-only-password-123"
GAMEYA_SITE = Path(__file__).resolve().parents[2]
TEMPLATE_DIR = Path(__file__).resolve().parents[1] / "templates" / "circles"

# Long enough for Django's deploy check: at least 50 characters, and not a placeholder.
PRODUCTION_KEY = "test-only-key-" + "Qz7mR2vX9kL4pT8wB1nJ6sH3dF5gY0cA" * 2

GAMEYA_DATA = {
    "name": "New circle",
    "start_date": "2026-10-11",
    "weeks": 10,
    "per_week": 1,
    "share_value": 500,
}


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture
def organiser(db, django_user_model):
    return django_user_model.objects.create_user("organiser", "organiser@example.com", PASSWORD)


@pytest.fixture
def stranger(db, django_user_model):
    return django_user_model.objects.create_user("stranger", "stranger@example.com", PASSWORD)


@pytest.fixture
def staff(db, django_user_model):
    return django_user_model.objects.create_user(
        "staff", "staff@example.com", PASSWORD, is_staff=True
    )


@pytest.fixture
def circle(db, organiser):
    # Named "Mine" and organised by `organiser`. The tests change it, and check it afterwards.
    return circle_factories.GameyaFactory(name="Mine", organiser=organiser)


def token_auth(user):
    token, _ = Token.objects.get_or_create(user=user)
    return {"HTTP_AUTHORIZATION": f"Token {token.key}"}


def jwt_auth(token):
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


def login(api, password=PASSWORD):
    return api.post(
        reverse("api-jwt-token"),
        {"username": "organiser", "password": password},
        format="json",
    )


# Part 1: ownership. Anyone reads. Only staff creates. An organiser changes their own gameya
# and its members, and nothing else.
def test_organiser_can_rename_their_gameya(api, organiser, circle):
    url = reverse("gameya-detail", args=[circle.pk])
    response = api.patch(url, {"name": "Renamed"}, format="json", **token_auth(organiser))
    assert response.status_code == 200
    circle.refresh_from_db()
    assert circle.name == "Renamed"


def test_another_user_cannot_change_a_gameya_they_do_not_organise(api, stranger, circle):
    url = reverse("gameya-detail", args=[circle.pk])
    response = api.patch(url, {"name": "Renamed"}, format="json", **token_auth(stranger))
    assert response.status_code == 403
    circle.refresh_from_db()
    assert circle.name == "Mine"


def test_an_organiser_cannot_create_a_gameya(api, organiser):
    response = api.post(reverse("gameya-list"), GAMEYA_DATA, format="json", **token_auth(organiser))
    assert response.status_code == 403
    assert not Gameya.objects.filter(name="New circle").exists()


def test_an_anonymous_user_cannot_change_a_gameya(api, circle):
    url = reverse("gameya-detail", args=[circle.pk])
    response = api.patch(url, {"name": "Renamed"}, format="json")
    assert response.status_code == 401


def test_an_organiser_can_change_a_member_of_their_gameya(api, organiser, circle):
    member = circle_factories.MemberFactory(gameya=circle, name="Ali")
    url = reverse("member-detail", args=[member.pk])
    response = api.patch(url, {"name": "Ali B"}, format="json", **token_auth(organiser))
    assert response.status_code == 200
    member.refresh_from_db()
    assert member.name == "Ali B"


def test_an_organiser_cannot_move_a_member_into_someone_elses_gameya(
    api, organiser, stranger, circle
):
    # Checking the member is not enough: the new gameya must be one the organiser owns too.
    theirs = circle_factories.GameyaFactory(name="Theirs", organiser=stranger)
    member = circle_factories.MemberFactory(gameya=circle, name="Ali")
    url = reverse("member-detail", args=[member.pk])
    response = api.patch(url, {"gameya": theirs.pk}, format="json", **token_auth(organiser))
    assert response.status_code == 403
    member.refresh_from_db()
    assert member.gameya_id == circle.pk


# Part 2: JWT. A login returns two tokens. The access token is short-lived and goes in the
# Authorization header as "Bearer <token>". The refresh token only buys a new access token.
def test_login_returns_an_access_and_a_refresh_token(api, organiser):
    response = login(api)
    assert response.status_code == 200
    assert {"access", "refresh"} <= response.json().keys()


def test_a_wrong_password_gets_no_tokens(api, organiser):
    response = login(api, password="wrong-password")
    assert response.status_code == 401
    assert "access" not in response.json()


def test_the_access_token_authorises_a_write(api, organiser, circle):
    access = login(api).json()["access"]
    url = reverse("gameya-detail", args=[circle.pk])
    response = api.patch(url, {"name": "Via JWT"}, format="json", **jwt_auth(access))
    assert response.status_code == 200
    circle.refresh_from_db()
    assert circle.name == "Via JWT"


def test_a_refresh_token_is_refused_as_an_access_token(api, organiser, circle):
    refresh = str(RefreshToken.for_user(organiser))
    url = reverse("gameya-detail", args=[circle.pk])
    response = api.patch(url, {"name": "x"}, format="json", **jwt_auth(refresh))
    assert response.status_code == 401


def test_an_expired_access_token_is_refused(api, organiser, circle):
    access = AccessToken.for_user(organiser)
    access.set_exp(lifetime=timedelta(seconds=-1))
    url = reverse("gameya-detail", args=[circle.pk])
    response = api.patch(url, {"name": "x"}, format="json", **jwt_auth(str(access)))
    assert response.status_code == 401


def test_the_refresh_endpoint_returns_a_new_access_token(api, organiser):
    refresh = str(RefreshToken.for_user(organiser))
    response = api.post(reverse("api-jwt-refresh"), {"refresh": refresh}, format="json")
    assert response.status_code == 200
    assert "access" in response.json()


# Part 3: CSRF. A form that a browser posts with a session needs a token. A token API does not:
# the browser does not add a token header by itself, so a forged page cannot send one.
def payment_data(member):
    return {"member": member.pk, "week": 1, "paid_on": "2026-10-11", "amount": member.due()}


def test_a_payment_form_post_without_a_csrf_token_is_refused(circle):
    member = circle_factories.MemberFactory(gameya=circle, name="Ali")
    client = Client(enforce_csrf_checks=True)
    url = reverse("gameya_payments", args=[circle.pk])
    response = client.post(url, payment_data(member))
    assert response.status_code == 403
    assert not Payment.objects.exists()


def test_a_payment_form_post_with_the_csrf_token_is_accepted(circle):
    member = circle_factories.MemberFactory(gameya=circle, name="Ali")
    client = Client(enforce_csrf_checks=True)
    # The admin login page is a real form: it sets the CSRF cookie and carries the token.
    page = client.get(reverse("admin:login"))
    token = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', page.content.decode())
    url = reverse("gameya_payments", args=[circle.pk])
    response = client.post(url, {**payment_data(member), "csrfmiddlewaretoken": token.group(1)})
    assert response.status_code == 201


def test_a_token_api_write_needs_no_csrf_token(staff):
    api = APIClient(enforce_csrf_checks=True)
    response = api.post(reverse("gameya-list"), GAMEYA_DATA, format="json", **token_auth(staff))
    assert response.status_code == 201


# Part 4: XSS. Django escapes a value in a template, so a script in a member's name is shown as
# text. The templates must not switch that escaping off.
def test_a_member_name_with_a_script_is_shown_as_text(circle):
    circle_factories.MemberFactory(gameya=circle, name="<script>alert('x')</script>")
    client = Client()
    html = client.get(reverse("gameya_page", args=[circle.pk])).content.decode()
    assert "<script>alert" not in html
    assert "&lt;script&gt;" in html


def test_the_templates_keep_escaping_on():
    for name in ("base.html", "gameya_detail.html"):
        source = (TEMPLATE_DIR / name).read_text(encoding="utf-8")
        assert "|safe" not in source, name
        assert "autoescape off" not in source, name


# Part 5: production settings. Django's own deploy checks must pass, and the app must refuse to
# start without a secret key. Each test starts manage.py in a new process, with its own settings.
def run_manage(*args, **env):
    clean = {name: value for name, value in os.environ.items() if not name.startswith("DJANGO_")}
    clean.update(env)
    return subprocess.run(
        [sys.executable, "manage.py", *args],
        cwd=GAMEYA_SITE,
        env=clean,
        capture_output=True,
        text=True,
        timeout=120,
    )


def test_production_settings_pass_the_django_deploy_checks():
    result = run_manage(
        "check",
        "--deploy",
        DJANGO_PRODUCTION="1",
        DJANGO_SECRET_KEY=PRODUCTION_KEY,
        DJANGO_ALLOWED_HOSTS="gameya.example.com",
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "no issues" in result.stdout


def test_production_refuses_to_start_without_a_secret_key():
    result = run_manage("check", DJANGO_PRODUCTION="1", DJANGO_ALLOWED_HOSTS="gameya.example.com")
    assert result.returncode != 0
    assert "DJANGO_SECRET_KEY" in result.stdout + result.stderr
