"""URLs for the circles app. Modules 01 and 04: connect each URL to a view, and name it."""

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
]
