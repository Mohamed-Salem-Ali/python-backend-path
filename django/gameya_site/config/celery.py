"""The Celery app for this project. Module 10.

Celery runs tasks outside the web request. It needs to know two things: where Django's settings
are, and where the tasks live. This file creates the app. config/__init__.py imports it, so the
app loads whenever Django starts.
"""

# TODO 35 (module 10): create the Celery app and connect it to Django.
#          Name the app "gameya". Load its configuration from Django's settings, reading only the
#          settings whose names start with CELERY_. Then tell it to look for a tasks module in
#          every installed app. The lesson, section 3, walks through each step.
#          Until this is written, `app` is None, and the Celery tests fail.
app = None
