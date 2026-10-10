"""Module 10 acceptance tests: the Celery app, the schedule, and the report tasks. Do not edit.

Run (from django/gameya_site):  pytest circles/tests/test_tasks.py

They need config/celery.py (TODO 35), config/__init__.py (TODO 36), the Celery settings (TODO 37)
and circles/tasks.py (TODO 38). The report reads unpaid members with unpaid_members from module
02, so that function must work too.
"""

from datetime import timedelta

import pytest
from config.celery import app
from django.conf import settings
from django.utils import timezone

from circles import tasks
from circles.tasks import current_week, queue_unpaid_reports, send_unpaid_report
from circles.tests import factories as circle_factories

# Names the report can contain. Karim is the only one who paid week 1 in the fixture below.
NAMES = {"Ali", "Bassem", "Sara", "Karim"}


@pytest.fixture
def running_circle(db):
    # Starts today, so week 1 has begun. Karim has paid week 1. Ali, Sara and Bassem have not.
    today = timezone.localdate()
    gameya = circle_factories.GameyaFactory(name="Friday circle", start_date=today, weeks=10)
    karim = circle_factories.MemberFactory(gameya=gameya, name="Karim")
    circle_factories.PaymentFactory(member=karim, week=1)
    for name in ("Sara", "Ali", "Bassem"):
        circle_factories.MemberFactory(gameya=gameya, name=name)
    return gameya


# Part 1: the Celery app and the schedule.
def test_celery_app_is_named_gameya():
    assert app.main == "gameya"


def test_celery_app_reads_celery_settings_from_django():
    # The test run is eager (see CELERY_TASK_ALWAYS_EAGER in settings): tasks run in this process.
    assert app.conf.task_always_eager is True
    assert app.conf.task_eager_propagates is False


def test_package_exposes_the_celery_app():
    # Imported inside the test: until TODO 36 is done, this import fails, and only this test fails.
    from config import celery_app

    assert celery_app is app


def test_beat_schedule_queues_the_reports():
    scheduled = [entry["task"] for entry in settings.CELERY_BEAT_SCHEDULE.values()]
    assert "circles.tasks.queue_unpaid_reports" in scheduled


def test_both_tasks_are_registered_with_the_app():
    assert "circles.tasks.send_unpaid_report" in app.tasks
    assert "circles.tasks.queue_unpaid_reports" in app.tasks


# Part 2: which week a gameya is in today. Week 1 is the first seven days, from the start date.
def test_current_week_is_none_before_the_start():
    today = timezone.localdate()
    gameya = circle_factories.GameyaFactory.build(start_date=today + timedelta(days=1))
    assert current_week(gameya, today) is None


def test_week_one_starts_on_the_start_date():
    today = timezone.localdate()
    gameya = circle_factories.GameyaFactory.build(start_date=today, weeks=10)
    assert current_week(gameya, today) == 1


def test_week_changes_every_seven_days():
    today = timezone.localdate()
    gameya = circle_factories.GameyaFactory.build(start_date=today - timedelta(days=6), weeks=10)
    assert current_week(gameya, today) == 1  # the seventh day is still week 1
    gameya.start_date = today - timedelta(days=7)
    assert current_week(gameya, today) == 2


def test_current_week_is_none_after_the_last_week():
    today = timezone.localdate()
    gameya = circle_factories.GameyaFactory.build(start_date=today - timedelta(days=13), weeks=2)
    assert current_week(gameya, today) == 2  # the last day of a two-week circle
    gameya.start_date = today - timedelta(days=14)
    assert current_week(gameya, today) is None


# Part 3: the report task. It runs right away here, because of eager mode.
def test_report_emails_the_organiser_the_unpaid_names(running_circle, mailoutbox):
    send_unpaid_report.delay(running_circle.pk, 1).get()
    assert len(mailoutbox) == 1
    message = mailoutbox[0]
    assert message.to == [settings.GAMEYA_ORGANISER_EMAIL]
    assert "Friday circle" in message.subject
    assert "week 1" in message.subject
    # One line per unpaid member, sorted by name. Karim paid, so he is not on the list.
    names = [line.strip() for line in message.body.splitlines() if line.strip() in NAMES]
    assert names == ["Ali", "Bassem", "Sara"]


def test_report_returns_how_many_are_unpaid(running_circle):
    assert send_unpaid_report.delay(running_circle.pk, 1).get() == 3


def test_report_sends_nothing_when_everyone_has_paid(running_circle, mailoutbox):
    for member in list(running_circle.members.exclude(payments__week=1)):
        circle_factories.PaymentFactory(member=member, week=1)
    assert send_unpaid_report.delay(running_circle.pk, 1).get() == 0
    assert mailoutbox == []


def test_report_retries_when_the_mail_server_is_down(running_circle, monkeypatch):
    calls = []

    def flaky_send_mail(*args, **kwargs):
        calls.append(1)
        if len(calls) < 3:
            raise OSError("mail server is down")

    monkeypatch.setattr(tasks, "send_mail", flaky_send_mail)
    assert send_unpaid_report.delay(running_circle.pk, 1).get() == 3
    assert len(calls) == 3  # two failures, then a success


def test_report_gives_up_after_three_retries(running_circle, monkeypatch):
    calls = []

    def dead_send_mail(*args, **kwargs):
        calls.append(1)
        raise OSError("mail server is down")

    monkeypatch.setattr(tasks, "send_mail", dead_send_mail)
    with pytest.raises(OSError):
        send_unpaid_report.delay(running_circle.pk, 1).get()
    assert len(calls) == 4  # the first try and three retries


# Part 4: the job that the schedule runs. It queues one report per gameya that is running today.
def test_queue_sends_one_report_per_running_circle(running_circle, mailoutbox):
    today = timezone.localdate()
    circle_factories.GameyaFactory(
        name="Old circle", start_date=today - timedelta(days=100), weeks=2
    )
    circle_factories.GameyaFactory(name="Next circle", start_date=today + timedelta(days=5))
    assert queue_unpaid_reports.delay().get() == 1
    assert len(mailoutbox) == 1
    assert "Friday circle" in mailoutbox[0].subject


def test_queue_returns_zero_when_no_circle_is_running(db, mailoutbox):
    today = timezone.localdate()
    circle_factories.GameyaFactory(start_date=today + timedelta(days=5))
    assert queue_unpaid_reports.delay().get() == 0
    assert mailoutbox == []
