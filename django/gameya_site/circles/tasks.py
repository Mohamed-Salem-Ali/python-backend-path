"""Background tasks: work that runs later, outside the web request. Module 10.

A task is a function that Celery can run later, in a worker process. Here the tasks email the
organiser the names of members who have not paid. In tests and local work the settings run each
task at once, in this process (eager mode), so a test can call it and check the result.
The lesson, section 4, explains the arguments each task takes and why.
"""

from datetime import date  # noqa: F401  (you will use it)

from celery import shared_task  # noqa: F401  (you will use it)
from django.conf import settings  # noqa: F401  (you will use it)
from django.core.mail import send_mail  # noqa: F401  (you will use it)
from django.utils import timezone  # noqa: F401  (you will use it)

from .models import Gameya  # noqa: F401  (you will use it)
from .queries import unpaid_members  # noqa: F401  (you will use it)


# TODO 38a: current_week(gameya, today) returns the week of the gameya that `today` falls in,
#           counting from 1, or None when the gameya has not started yet or has already ended.
#           Week 1 is the first seven days, counting from the start date. The gameya has
#           `weeks` weeks. Use integer division on the number of days since the start.
def current_week(gameya, today):
    """The week that `today` falls in, or None when the gameya is not running."""
    raise NotImplementedError("TODO 38a")


# TODO 38b: send_unpaid_report(gameya_id, week) is a task. It returns how many members have not
#           paid that week, and sends one email about them:
#             - recipient: settings.GAMEYA_ORGANISER_EMAIL, as a list with one address
#             - subject: the gameya's name and the week, for example
#               "Unpaid for week 1: Friday circle"
#             - body: one line per unpaid member, containing only the name, sorted by name
#             - no email at all when everyone has paid; still return 0
#           Load the gameya by its id, not from an object passed in. Use unpaid_members (module
#           02) with today's date from timezone.localdate().
#           Retries: if sending fails with OSError (the mail server is down), try again. Allow
#           three retries, so four tries in all, and let the last error reach the caller. Two
#           settings on the decorator do this: autoretry_for names the exceptions that trigger a
#           retry, and max_retries sets the limit. Read the lesson, section 6.
@shared_task
def send_unpaid_report(gameya_id, week):
    """Email the organiser who has not paid this week, and return how many."""
    raise NotImplementedError("TODO 38b")


# TODO 38c: queue_unpaid_reports() is the job the schedule runs. For every gameya that is running
#           today (current_week is not None), queue one send_unpaid_report for that gameya and its
#           current week. Queue with .delay(...). Return how many reports it queued, so a gameya
#           that has not started or has ended queues nothing.
@shared_task
def queue_unpaid_reports():
    """Queue one unpaid report for every gameya that is running today."""
    raise NotImplementedError("TODO 38c")
