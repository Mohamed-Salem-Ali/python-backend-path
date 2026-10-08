"""Views: functions and classes that take a request and return a response.

Modules 01 (function views) and 04 (class-based views).
"""

from django.http import HttpRequest, HttpResponse, JsonResponse  # noqa: F401
from django.shortcuts import get_object_or_404, render  # noqa: F401
from django.views import View  # noqa: F401
from django.views.decorators.http import require_GET  # noqa: F401
from django.views.generic import DetailView, ListView  # noqa: F401

# Add the app's imports as you need them, for example:
#   from .forms import PaymentForm
#   from .models import Gameya, Payment
# Do not import a name before it exists: a failed import here breaks every view in this file,
# including the module 01 views.


# TODO 1: health(request) -> JsonResponse({"status": "ok"}). Only GET is allowed (405 otherwise).
# TODO 2: hello(request, name) -> HttpResponse("Hello, <name>!")
# TODO 3: add(request, a, b) -> JsonResponse({"sum": a + b})
# TODO 4: about(request) renders "circles/about.html" with the context {"title": "About Gameya"}.
#         Create that template yourself in circles/templates/circles/about.html.

# Module 04: class-based views. Each one returns JSON for now; module 05 adds HTML pages.
# Pair each view with its route in urls.py, then run its test class:
#   TODO 5 with TODO 8  (GameyaList,     test class GameyaListTests)
#   TODO 6 with TODO 9  (GameyaDetail,   test class GameyaDetailTests)
#   TODO 7 with TODO 10 (GameyaPayments, test class GameyaPaymentsTests)

# TODO 5: class GameyaList(View). Its get() returns every gameya ordered by name, as a JSON list
#         of {id, name, weeks, share_value}. A ?q= query parameter keeps only the names that
#         contain it, ignoring case: use the icontains lookup, not contains. Read it with
#         request.GET.get("q", "").
# TODO 6: class GameyaDetail(DetailView), with model = Gameya. Override render_to_response() to
#         return JsonResponse of {id, name, weeks, per_week, share_value, turns, payout,
#         weekly_pot}. A gameya that does not exist is a 404, and DetailView handles that.
# TODO 7: class GameyaPayments(View). Its get() returns this gameya's payments in week order as
#         a JSON list of {id, member (the member's name), week, amount, paid_on (ISO date)}.
#         Load the members in the same query (select_related), so the page runs a fixed number
#         of queries however many payments there are.
#         Its post() builds a PaymentForm from request.POST. The member must belong to this
#         gameya: report that as an error on the "member" field. Valid: save and return 201 with
#         the payment's JSON. Invalid: return 400 with {"errors": form.errors.get_json_data()}.
#         A duplicate week comes back under the "__all__" key. Use get_object_or_404 for the
#         gameya.
