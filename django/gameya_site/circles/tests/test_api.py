"""Module 06 acceptance tests: the Gameya REST API with Django REST Framework. Do not edit.

Run:  python manage.py test circles.tests.test_api

These tests use the Module 02 models. They need djangorestframework and its authtoken app in
INSTALLED_APPS (see the lesson), and the serializers, viewsets and routes from Module 06.
"""

from datetime import date

from django.apps import apps
from django.contrib.auth import get_user_model
from django.test import SimpleTestCase
from django.urls import reverse
from rest_framework import serializers, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# Import the modules, not the names: a missing class then fails only the tests that use it.
from circles import api as circle_api
from circles import serializers as circle_serializers
from circles.models import Gameya, Member

PASSWORD = "test-only-password-123"


def make_gameya(**overrides):
    values = {
        "name": "Alpha",
        "start_date": date(2026, 10, 11),
        "weeks": 10,
        "per_week": 1,
        "share_value": 500,
    }
    values.update(overrides)
    return Gameya.objects.create(**values)


class ApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User = get_user_model()
        cls.staff = User.objects.create_user("staff", "staff@example.com", PASSWORD, is_staff=True)
        cls.reader = User.objects.create_user("reader", "reader@example.com", PASSWORD)
        cls.staff_token = Token.objects.create(user=cls.staff)
        cls.reader_token = Token.objects.create(user=cls.reader)

        # Created out of name order: the id order differs from the name order, so a view that
        # sorts by id fails the name-order tests.
        cls.beta = make_gameya(name="Beta", weeks=10, per_week=1, share_value=500)  # payout 5000
        cls.gamma = make_gameya(name="Gamma", weeks=12, per_week=1, share_value=300)  # payout 3600
        # Two payouts a week, so the weekly pot (per_week * payout) differs from the payout.
        cls.alpha = make_gameya(name="Alpha", weeks=8, per_week=2, share_value=200)
        # Ali has two shares at 200 a share: due 400. Sara has three: due 600.
        cls.ali = Member.objects.create(gameya=cls.alpha, name="Ali", shares=2)
        cls.sara = Member.objects.create(gameya=cls.alpha, name="Sara", shares=3)
        cls.omar = Member.objects.create(gameya=cls.beta, name="Omar", shares=1)

    def use_token(self, token=None):
        """Send a token in the Authorization header, or nothing for an anonymous request."""
        if token is None:
            self.client.credentials()
        else:
            self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")


class SetupTests(SimpleTestCase):
    def test_rest_framework_and_its_token_app_are_installed(self):
        self.assertTrue(apps.is_installed("rest_framework"))
        self.assertTrue(apps.is_installed("rest_framework.authtoken"))


class GameyaApiTests(ApiTestCase):
    def test_lists_gameyas_one_page_at_a_time(self):
        response = self.client.get(reverse("gameya-list"))
        self.assertEqual(response.status_code, 200)
        page = response.json()
        self.assertEqual(set(page), {"count", "next", "previous", "results"})
        self.assertEqual(page["count"], 3)
        self.assertEqual([item["name"] for item in page["results"]], ["Alpha", "Beta"])
        self.assertIsNotNone(page["next"])

        second = self.client.get(reverse("gameya-list"), {"page": 2}).json()
        self.assertEqual([item["name"] for item in second["results"]], ["Gamma"])
        self.assertIsNone(second["next"])

    def test_each_item_has_the_public_fields_and_figures(self):
        alpha = self.client.get(reverse("gameya-list")).json()["results"][0]
        self.assertEqual(
            alpha,
            {
                "id": self.alpha.pk,
                "name": "Alpha",
                "start_date": "2026-10-11",
                "weeks": 8,
                "per_week": 2,
                "share_value": 200,
                "turns": 16,
                "payout": 1600,
                "weekly_pot": 3200,
            },
        )

    def test_search_matches_part_of_the_name_ignoring_case(self):
        response = self.client.get(reverse("gameya-list"), {"search": "LPH"})
        self.assertEqual([item["name"] for item in response.json()["results"]], ["Alpha"])

    def test_ordering_by_weeks_descending(self):
        response = self.client.get(reverse("gameya-list"), {"ordering": "-weeks"})
        self.assertEqual(
            [item["name"] for item in response.json()["results"]],
            ["Gamma", "Beta"],
        )

    def test_a_field_that_is_not_in_ordering_fields_is_ignored(self):
        # share_value is not an ordering field, so the default order (by name) applies.
        response = self.client.get(reverse("gameya-list"), {"ordering": "-share_value"})
        self.assertEqual(
            [item["name"] for item in response.json()["results"]],
            ["Alpha", "Beta"],
        )

    def test_retrieve_returns_one_gameya_with_its_figures(self):
        response = self.client.get(reverse("gameya-detail", args=[self.beta.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "id": self.beta.pk,
                "name": "Beta",
                "start_date": "2026-10-11",
                "weeks": 10,
                "per_week": 1,
                "share_value": 500,
                "turns": 10,
                "payout": 5000,
                "weekly_pot": 5000,
            },
        )

    def test_the_members_action_lists_only_that_gameyas_members(self):
        response = self.client.get(reverse("gameya-members", args=[self.alpha.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            [
                {
                    "id": self.ali.pk,
                    "gameya": self.alpha.pk,
                    "name": "Ali",
                    "shares": 2,
                    "due": 400,
                },
                {
                    "id": self.sara.pk,
                    "gameya": self.alpha.pk,
                    "name": "Sara",
                    "shares": 3,
                    "due": 600,
                },
            ],
        )

    def test_the_members_action_for_a_missing_gameya_is_404(self):
        response = self.client.get(reverse("gameya-members", args=[999999]))
        self.assertEqual(response.status_code, 404)

    def test_reading_needs_no_token_and_head_and_options_are_allowed(self):
        self.use_token(None)
        url = reverse("gameya-list")
        self.assertEqual(self.client.head(url).status_code, 200)
        self.assertEqual(self.client.options(url).status_code, 200)

    def test_an_anonymous_user_cannot_create_a_gameya(self):
        self.use_token(None)
        response = self.client.post(
            reverse("gameya-list"), {"name": "X", "weeks": 2, "share_value": 10}
        )
        self.assertEqual(response.status_code, 401)
        self.assertFalse(Gameya.objects.filter(name="X").exists())

    def test_a_logged_in_user_who_is_not_staff_cannot_create_a_gameya(self):
        self.use_token(self.reader_token)
        response = self.client.post(
            reverse("gameya-list"), {"name": "X", "weeks": 2, "share_value": 10}
        )
        self.assertEqual(response.status_code, 403)
        self.assertFalse(Gameya.objects.filter(name="X").exists())

    def test_staff_can_create_a_gameya_and_per_week_defaults_to_one(self):
        self.use_token(self.staff_token)
        response = self.client.post(
            reverse("gameya-list"),
            {"name": "Delta", "start_date": "2026-11-01", "weeks": 4, "share_value": 250},
        )
        self.assertEqual(response.status_code, 201)
        saved = Gameya.objects.get(name="Delta")
        self.assertEqual(
            response.json(),
            {
                "id": saved.pk,
                "name": "Delta",
                "start_date": "2026-11-01",
                "weeks": 4,
                "per_week": 1,
                "share_value": 250,
                "turns": 4,
                "payout": 1000,
                "weekly_pot": 1000,
            },
        )

    def test_weeks_per_week_and_share_value_must_be_at_least_one(self):
        self.use_token(self.staff_token)
        for field in ("weeks", "per_week", "share_value"):
            with self.subTest(field=field):
                data = {
                    "name": "Zero",
                    "start_date": "2026-11-01",
                    "weeks": 4,
                    "share_value": 250,
                    field: 0,
                }
                response = self.client.post(reverse("gameya-list"), data)
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.json())
        self.assertFalse(Gameya.objects.filter(name="Zero").exists())

    def test_staff_can_change_and_delete_a_gameya(self):
        self.use_token(self.staff_token)
        url = reverse("gameya-detail", args=[self.gamma.pk])
        response = self.client.patch(url, {"name": "Gamma Two"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["name"], "Gamma Two")

        self.assertEqual(self.client.delete(url).status_code, 204)
        self.assertFalse(Gameya.objects.filter(pk=self.gamma.pk).exists())

    def test_a_user_who_is_not_staff_cannot_change_a_gameya(self):
        self.use_token(self.reader_token)
        response = self.client.patch(
            reverse("gameya-detail", args=[self.gamma.pk]), {"name": "Hacked"}
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Gameya.objects.get(pk=self.gamma.pk).name, "Gamma")

    def test_the_api_root_lists_the_endpoints(self):
        response = self.client.get(reverse("api-root"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.json()), {"gameyas", "members"})

    def test_the_routes_are_under_api(self):
        self.assertEqual(reverse("gameya-list"), "/api/gameyas/")
        self.assertEqual(reverse("api-token"), "/api/token/")


class MemberApiTests(ApiTestCase):
    def test_lists_every_member_when_there_is_no_filter(self):
        response = self.client.get(reverse("member-list"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)  # not paginated
        self.assertEqual([m["name"] for m in response.json()], ["Ali", "Sara", "Omar"])

    def test_filters_by_gameya(self):
        response = self.client.get(reverse("member-list"), {"gameya": self.alpha.pk})
        self.assertEqual([m["name"] for m in response.json()], ["Ali", "Sara"])

    def test_a_gameya_filter_that_is_not_a_whole_number_in_range_is_a_400(self):
        # isdigit() accepts "²" and then int() fails. A huge number overflows the database.
        for value in ("abc", "", "1.5", "-1", "²", "99999999999999999999"):
            with self.subTest(value=value):
                response = self.client.get(reverse("member-list"), {"gameya": value})
                self.assertEqual(response.status_code, 400)

    def test_the_list_loads_each_members_gameya_in_the_same_query(self):
        # Without select_related("gameya"), each member's due reloads its gameya.
        with self.assertNumQueries(1):
            self.client.get(reverse("member-list"))

    def test_staff_can_add_a_member_and_the_due_is_computed(self):
        self.use_token(self.staff_token)
        response = self.client.post(
            reverse("member-list"),
            {"gameya": self.beta.pk, "name": "Lina", "shares": 2},
        )
        self.assertEqual(response.status_code, 201)
        saved = Member.objects.get(name="Lina")
        self.assertEqual(
            response.json(),
            {"id": saved.pk, "gameya": self.beta.pk, "name": "Lina", "shares": 2, "due": 1000},
        )

    def test_shares_default_to_one_and_due_is_still_computed(self):
        self.use_token(self.staff_token)
        response = self.client.post(
            reverse("member-list"),
            {"gameya": self.beta.pk, "name": "Pia", "due": 1},
        )
        self.assertEqual(response.status_code, 201)
        saved = Member.objects.get(name="Pia")
        self.assertEqual(
            response.json(),
            {"id": saved.pk, "gameya": self.beta.pk, "name": "Pia", "shares": 1, "due": 500},
        )

    def test_a_duplicate_name_in_one_gameya_is_rejected(self):
        self.use_token(self.staff_token)
        response = self.client.post(
            reverse("member-list"),
            {"gameya": self.alpha.pk, "name": "Ali", "shares": 1},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Member.objects.filter(gameya=self.alpha, name="Ali").count(), 1)

    def test_the_same_name_is_allowed_in_another_gameya(self):
        self.use_token(self.staff_token)
        response = self.client.post(
            reverse("member-list"),
            {"gameya": self.beta.pk, "name": "Ali", "shares": 1},
        )
        self.assertEqual(response.status_code, 201)

    def test_shares_must_be_at_least_one(self):
        self.use_token(self.staff_token)
        response = self.client.post(
            reverse("member-list"),
            {"gameya": self.beta.pk, "name": "Lina", "shares": 0},
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("shares", response.json())

    def test_an_anonymous_user_cannot_add_a_member(self):
        self.use_token(None)
        response = self.client.post(
            reverse("member-list"),
            {"gameya": self.beta.pk, "name": "Lina", "shares": 1},
        )
        self.assertEqual(response.status_code, 401)
        self.assertFalse(Member.objects.filter(name="Lina").exists())

    def test_a_user_who_is_not_staff_cannot_delete_a_member(self):
        self.use_token(self.reader_token)
        response = self.client.delete(reverse("member-detail", args=[self.ali.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Member.objects.filter(pk=self.ali.pk).exists())


class TokenTests(ApiTestCase):
    def test_a_username_and_password_give_a_token(self):
        self.use_token(None)
        response = self.client.post(
            reverse("api-token"), {"username": "staff", "password": PASSWORD}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"token": self.staff_token.key})

    def test_a_wrong_password_gets_no_token(self):
        self.use_token(None)
        response = self.client.post(
            reverse("api-token"), {"username": "staff", "password": "wrong"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertNotIn("token", response.json())


class ApiStructureTests(ApiTestCase):
    def test_the_views_are_viewsets_and_the_data_is_serialized_by_model_serializers(self):
        self.assertTrue(issubclass(circle_api.GameyaViewSet, viewsets.ModelViewSet))
        self.assertTrue(issubclass(circle_api.MemberViewSet, viewsets.ModelViewSet))
        self.assertTrue(
            issubclass(circle_serializers.GameyaSerializer, serializers.ModelSerializer)
        )
        self.assertTrue(
            issubclass(circle_serializers.MemberSerializer, serializers.ModelSerializer)
        )

    def test_turns_payout_and_weekly_pot_are_read_only(self):
        serializer = circle_serializers.GameyaSerializer(
            data={
                "name": "X",
                "start_date": "2026-10-11",
                "weeks": 2,
                "share_value": 10,
                "turns": 99,
                "payout": 99,
                "weekly_pot": 99,
            }
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertNotIn("turns", serializer.validated_data)
        self.assertNotIn("payout", serializer.validated_data)
        self.assertNotIn("weekly_pot", serializer.validated_data)
