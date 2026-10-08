from django.apps import AppConfig


class CirclesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "circles"

    # TODO 25: add a ready() method that imports the signals module. Django calls ready() once,
    #          when the server or the tests start. Without that import, the receivers are never
    #          connected, and no audit entry is written. Do not import the module at the top of
    #          this file: the app registry is not ready there, and the import fails.
