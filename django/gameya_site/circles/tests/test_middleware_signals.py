"""Module 07 acceptance tests: middleware and signals. Do not edit.

Run:  python manage.py test circles.tests.test_middleware_signals

The RequestIdMiddlewareTests class needs only the middleware (TODO 23) and the settings entry
(TODO 27). The AuditTests class also needs the AuditEntry model (TODO 26), the receivers
(TODO 24) and ready() (TODO 25). The Module 02 models and the Module 06 route "api-root" must
exist too.
"""

from datetime import date

from django.conf import settings
from django.db import IntegrityError, connection, transaction
from django.http import HttpResponse
from django.test import RequestFactory, TestCase, override_settings
from django.test.utils import CaptureQueriesContext
from django.urls import reverse

# Import the modules, not the names: a missing model or class then fails only the tests that use it.
from circles import middleware as circle_middleware
from circles import models as circle_models
from circles.models import Gameya, Member, Payment

HEX_32 = r"^[0-9a-f]{32}$"


class RequestIdMiddlewareTests(TestCase):
    def test_the_middleware_is_the_first_entry_in_settings(self):
        self.assertEqual(settings.MIDDLEWARE[0], "circles.middleware.RequestIdMiddleware")

    def test_every_response_has_a_32_character_request_id(self):
        response = self.client.get(reverse("api-root"))
        self.assertEqual(response.status_code, 200)
        self.assertRegex(response["X-Request-ID"], HEX_32)

    def test_a_404_response_has_one_too(self):
        # The middleware sees the response after the view, so error pages get the header too.
        response = self.client.get("/no-such-page/")
        self.assertEqual(response.status_code, 404)
        self.assertRegex(response["X-Request-ID"], HEX_32)

    @override_settings(SECURE_SSL_REDIRECT=True)
    def test_a_redirect_from_security_middleware_has_one_too(self):
        # SecurityMiddleware answers this request with a redirect before any view runs. The
        # header is still there only if our middleware is outside SecurityMiddleware.
        response = self.client.get("/", secure=False)
        self.assertEqual(response.status_code, 301)
        self.assertRegex(response["X-Request-ID"], HEX_32)

    def test_each_request_gets_its_own_id(self):
        first = self.client.get(reverse("api-root"))["X-Request-ID"]
        second = self.client.get(reverse("api-root"))["X-Request-ID"]
        self.assertNotEqual(first, second)

    def test_a_valid_incoming_id_is_echoed_on_the_request_and_the_header(self):
        # The lengths 1 and 64 are the two edges of the rule. "abc-123_XYZ" mixes all three
        # kinds of allowed character.
        for value in ("a", "abc-123_XYZ", "y" * 64):
            with self.subTest(value=value):
                seen = {}

                def view(request):
                    seen["id"] = request.request_id
                    return HttpResponse("ok")

                response = circle_middleware.RequestIdMiddleware(view)(
                    RequestFactory().get("/", HTTP_X_REQUEST_ID=value)
                )
                self.assertEqual(seen["id"], value)
                self.assertEqual(response["X-Request-ID"], value)

    def test_an_invalid_incoming_id_is_replaced_on_the_request_and_the_header(self):
        # Empty, spaces, a semicolon, a dot, a newline, a non-ASCII letter, and 65 characters.
        for value in ("", "bad id", "semi;colon", "a.b", "abc\n", "café", "x" * 65):
            with self.subTest(value=value):
                seen = {}

                def view(request):
                    seen["id"] = request.request_id
                    return HttpResponse("ok")

                response = circle_middleware.RequestIdMiddleware(view)(
                    RequestFactory().get("/", HTTP_X_REQUEST_ID=value)
                )
                self.assertNotEqual(seen["id"], value)
                self.assertRegex(seen["id"], HEX_32)
                self.assertEqual(response["X-Request-ID"], seen["id"])

    def test_a_new_id_is_stored_on_the_request_too(self):
        seen = {}

        def view(request):
            seen["id"] = request.request_id
            return HttpResponse("ok")

        response = circle_middleware.RequestIdMiddleware(view)(RequestFactory().get("/"))
        self.assertRegex(seen["id"], HEX_32)
        self.assertEqual(response["X-Request-ID"], seen["id"])


class AuditTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.gameya = Gameya.objects.create(
            name="Alpha", start_date=date(2026, 10, 11), weeks=10, share_value=500
        )
        # Creating a member is not audited. Ali is the member whose payments the tests use.
        cls.ali = Member.objects.create(gameya=cls.gameya, name="Ali", shares=2)

    def entries(self):
        return circle_models.AuditEntry.objects.order_by("id")

    def rows(self):
        return [(e.action, e.model, e.object_id, e.summary) for e in self.entries()]

    def make_payment(self, member=None, week=3, pk=None):
        return Payment.objects.create(
            pk=pk,
            member=member or self.ali,
            week=week,
            paid_on=date(2026, 10, 11),
            amount=1000,
        )

    def test_creating_a_payment_writes_one_created_entry(self):
        self.make_payment(pk=77)
        self.assertEqual(self.rows(), [("created", "payment", 77, "Ali: week 3")])
        self.assertIsNotNone(self.entries().get().created_at)

    def test_changing_a_payment_writes_nothing(self):
        payment = self.make_payment(pk=77)
        payment.amount = 1200
        payment.save()
        self.assertEqual(self.rows(), [("created", "payment", 77, "Ali: week 3")])

    def test_deleting_a_payment_writes_a_deleted_entry(self):
        payment = self.make_payment(pk=77)
        payment.delete()
        self.assertEqual(
            self.rows(),
            [
                ("created", "payment", 77, "Ali: week 3"),
                ("deleted", "payment", 77, "Ali: week 3"),
            ],
        )

    def test_deleting_a_member_writes_a_deleted_entry_for_the_member(self):
        sara = Member.objects.create(gameya=self.gameya, name="Sara", shares=1)
        sara_pk = sara.pk
        sara.delete()
        self.assertEqual(self.rows(), [("deleted", "member", sara_pk, "Sara (Alpha)")])

    def test_deleting_a_member_with_a_payment_audits_the_payment_then_the_member(self):
        # Deleting a member also deletes its payments, and each deletion is audited.
        omar = Member.objects.create(gameya=self.gameya, name="Omar", shares=1)
        self.make_payment(member=omar, week=2, pk=78)
        omar_pk = omar.pk
        omar.delete()
        self.assertEqual(
            self.rows(),
            [
                ("created", "payment", 78, "Omar: week 2"),
                ("deleted", "payment", 78, "Omar: week 2"),
                ("deleted", "member", omar_pk, "Omar (Alpha)"),
            ],
        )

    def test_payout_slots_and_gameyas_are_not_audited(self):
        circle_models.PayoutSlot.objects.create(gameya=self.gameya, turn_number=1)
        empty = Gameya.objects.create(
            name="Empty", start_date=date(2026, 10, 11), weeks=2, share_value=100
        )
        empty.delete()
        self.assertEqual(self.rows(), [])

    def test_a_save_that_the_database_rejects_writes_no_entry(self):
        # A second payment for the same week breaks the unique rule. The database rejects the
        # row, so the INSERT for the audit entry must never be sent.
        self.make_payment(pk=77)
        with CaptureQueriesContext(connection) as queries:
            with self.assertRaises(IntegrityError), transaction.atomic():
                self.make_payment(pk=78)
        audit_inserts = [
            q["sql"]
            for q in queries.captured_queries
            if 'INSERT INTO "circles_auditentry"' in q["sql"]
        ]
        self.assertEqual(audit_inserts, [])
        self.assertEqual(self.rows(), [("created", "payment", 77, "Ali: week 3")])

    def test_the_audit_log_is_ordered_by_id(self):
        self.assertEqual(circle_models.AuditEntry._meta.ordering, ["id"])
