"""URLs for the circles app. Modules 01, 04, 05 and 06: connect each URL to a view, and name it."""

from django.urls import path  # noqa: F401  (you will use it)

# from . import views

# Give every route a plain name: the tests use reverse("health"), reverse("hello", args=["Sara"]).
urlpatterns = [
    # TODO: path("health/", views.health, name="health"),
    # TODO: "hello/<str:name>/" (name "hello"), "add/<int:a>/<int:b>/" (name "add"),
    #       and "about/" (name "about")
    # Module 04: the class-based views. Call .as_view() on each one.
    # TODO 8:  "gameyas/" (name "gameya_list")
    # TODO 9:  "gameyas/<int:pk>/" (name "gameya_detail")
    # TODO 10: "gameyas/<int:pk>/payments/" (name "gameya_payments")
    # Module 05: the HTML pages. Call .as_view() on each one.
    # TODO 13: "" (name "home"), the GameyaHome view
    # TODO 14: "gameyas/<int:pk>/page/" (name "gameya_page"), the GameyaPage view
    # Module 06: the REST API. Import include from django.urls, DefaultRouter from
    # rest_framework.routers, obtain_auth_token from rest_framework.authtoken.views, and
    # the api module (from . import api) at the top of this file.
    # TODO 22: router = DefaultRouter(). Register the viewsets from api.py:
    #          "gameyas" (basename "gameya") and "members" (basename "member").
    #          Add path("api/", include(router.urls)), and path("api/token/",
    #          obtain_auth_token, name="api-token").
    #          Do this last, after TODO 20 and 21. register() needs both viewsets to exist.
    #          Until then the whole project fails to start, and every module's tests fail with it.
]
