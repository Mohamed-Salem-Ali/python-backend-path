"""Views: functions that take a request and return a response. Module 01."""

from django.http import HttpRequest, HttpResponse, JsonResponse  # noqa: F401
from django.shortcuts import render  # noqa: F401
from django.views.decorators.http import require_GET  # noqa: F401


# TODO 1: health(request) -> JsonResponse({"status": "ok"}). Only GET is allowed (405 otherwise).
# TODO 2: hello(request, name) -> HttpResponse("Hello, <name>!")
# TODO 3: add(request, a, b) -> JsonResponse({"sum": a + b})
# TODO 4: about(request) renders "circles/about.html" with the context {"title": "About Gameya"}.
#         Create that template yourself in circles/templates/circles/about.html.
