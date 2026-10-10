# Module 10 (Django): Background tasks with Celery

By the end you can move slow or unreliable work out of a web request, write it as a Celery task, test it in eager mode, retry it when a service is down, and schedule it with Celery beat.

**Before you start:** finish modules 02 to 09. This module uses `unpaid_members` from module 02, the factories from module 08, and the test habits from module 09.

**Setup:** this module adds Celery to the project. Install the requirements again from `django/gameya_site`:

```bash
pip install -r requirements.txt
```

Run this module's tests from the same folder with `pytest circles/tests/test_tasks.py`. The tests are the specification. All 16 should pass when you finish.

**How to read the examples:** the examples use a made-up `newsletter` app with one model, `Subscriber` (a name and an email). It is not part of gameya_site. Learn the pattern here, then apply it to Gameya.

## 1. Why work moves out of the request
A web request should finish in well under a second. A user who clicks "Send reminders" should not wait while the server sends twenty emails, calls a slow API, or waits for a mail server that is down. Work that does not need to finish before the page answers can run later:

- the request answers at once, for example "reminders queued"
- a separate process does the work
- if the work fails, it can be tried again without anyone clicking anything

Keep work in the request when the user needs the result on the same page. Move it out when the user does not have to wait for it.

## 2. Four moving parts
- **Broker:** a queue that holds the messages. Production systems use Redis or RabbitMQ. This module uses `memory://`, which keeps the queue inside one process, so it only works for learning and tests.
- **Worker:** a process that takes messages from the broker and runs the matching function. Start it with `celery -A config worker`.
- **Beat:** a scheduler process. At set times it puts a task on the broker. It does not run tasks itself, so you need a worker as well.
- **Eager mode:** no broker and no worker. Calling a task runs it at once, in the same process, and returns a result you can read. Tests use it.

## 3. Connect Celery to Django
Celery knows nothing about your project until you tell it three things. Write them in `config/celery.py`:

1. An app, with a name. Use the project name.
2. Its settings come from Django's settings. Only names that start with `CELERY_` are read, so `CELERY_TASK_ALWAYS_EAGER` in `settings.py` becomes `task_always_eager` for Celery.
3. Discovery: look for a `tasks.py` file in every installed app.

The app must load whenever Django loads. Otherwise the `@shared_task` decorators in your modules do not know which app they belong to. So `config/__init__.py` imports the app.

**Try it:** in `python manage.py shell`, run `from config.celery import app`, then print `app.main` and `app.conf.task_always_eager`. Before TODO 35 and TODO 36 are done, you get an error. After them, you get the name you chose and the eager setting.

On Windows, start the worker with `--pool=solo`. Celery's default pool does not work on Windows. The solo pool runs one task at a time inside the worker process, which is enough for learning.

## 4. Write a task
A task is a function with the `@shared_task` decorator. Its name is its module path plus the function name, for example `circles.tasks.send_unpaid_report`.

```python
# Made-up example: a newsletter app, not part of gameya_site
from celery import shared_task
from django.core.mail import send_mail

from .models import Subscriber


@shared_task
def send_welcome(subscriber_id):
    subscriber = Subscriber.objects.get(pk=subscriber_id)
    send_mail("Welcome", f"Hi {subscriber.name}", None, [subscriber.email])
```

Three rules for the arguments:

- **Pass IDs and plain values, never model objects.** A message travels as text, so an object cannot be sent as it is. Even when it could, the row may change before the worker runs. Loading it inside the task gives the current data.
- **Keep the return value small.** A number or a short string is enough.
- **Plan for a second run.** A retry can run a task again after part of it has already worked. Ask what happens if the email went out and the code then failed. Would a second run send it twice?

**Try it:** open `circles/tasks.py`. For each of the three functions, list its arguments. Which ones take an ID, and which take a value that is not a model?

## 5. Run a task
- `send_welcome.delay(subscriber.pk)` is short for `send_welcome.apply_async(args=(subscriber.pk,))`. With a broker and a worker, it returns at once with a handle to the result.
- In eager mode, the task runs during the call. `.delay()` returns an `EagerResult`, and `.get()` gives you what the task returned.
- Errors: `CELERY_TASK_EAGER_PROPAGATES` decides whether an eager task raises at once. This project sets it to `False`, so an error comes out of `.get()`, the same way it would from a real result. Section 6 explains why that matters for retries.
- Production caveat: queue a task after the database commit. A task queued inside a transaction can run before the row exists. `transaction.on_commit(lambda: send_welcome.delay(subscriber.pk))` waits for the commit. The tests here do not need it, but read it before you combine Celery with writes.

**Try it:** in `python manage.py shell`, run `from circles.tasks import queue_unpaid_reports`, then `queue_unpaid_reports.delay().get()`. Once TODO 38c works, it prints how many reports were queued.

## 6. Retries
Retry only the errors that can go away. A mail server that is down (`OSError`) is worth another try. A bug, such as a gameya that does not exist, is not. Retrying a bug only repeats it, so let it fail.

Two settings on the decorator do the work:

- `autoretry_for=(OSError,)` names the exceptions that start a retry.
- `max_retries=3` sets how many retries follow the first try, so four tries in all.

When the limit is reached, the last error is raised. Then the result and your monitoring both see it.

Eager mode has one trap. With `CELERY_TASK_EAGER_PROPAGATES = True`, an eager retry raises Celery's `Retry` signal to the caller before the retry runs. With `False`, the retries run and the final error comes out of `.get()`. The test file expects `False`, which is why the settings TODO says so.

**Try it:** in the give-up test, the mail function is called four times. Find the line that checks this, and explain why it is four and not three.

## 7. Schedule with beat
`CELERY_BEAT_SCHEDULE` maps a name you choose to a task and a schedule:

```python
# Made-up example: the same newsletter app
CELERY_BEAT_SCHEDULE = {
    "send-welcome-digest": {
        "task": "newsletter.tasks.send_digest",
        "schedule": crontab(hour=8, minute=0),
    },
}
```

`crontab` runs at fixed times of the day. A `timedelta` runs at a fixed interval, for example every 30 seconds. Celery reads crontab times in the project's `TIME_ZONE` setting, so `crontab(hour=8)` means 08:00 in Cairo for this project.

Beat only queues. To see a scheduled run, start a worker and beat in two terminals. From `django/gameya_site`:

```bash
celery -A config worker -l info --pool=solo
```

```bash
celery -A config beat -l info
```

**Try it:** in a scratch copy of the project, change the schedule to `timedelta(seconds=30)`. Start both commands and watch the worker log for a task every 30 seconds. Then change the schedule back. Do not commit the scratch change.

## 8. Test tasks
- Eager mode keeps tests simple. Call `.delay(...).get()` and check the result.
- The `mailoutbox` fixture from pytest-django collects emails instead of sending them.
- To simulate a failing service, replace the function that the task calls with `monkeypatch.setattr(tasks, "send_mail", fake)`, and count the calls. Give the fake `*args, **kwargs` so the test does not depend on how the task calls `send_mail`.
- Test the schedule by reading `settings.CELERY_BEAT_SCHEDULE`. Running beat inside a test is slow and fragile.

Eager mode hides one kind of problem. A real worker runs in another process and cannot see your objects, so an object argument can pass every eager test and still fail in production. Pass IDs, and run one task through a real worker before you rely on it.

## 9. Project step: payment reminders for Gameya
The organiser needs to know who has not paid this week. You build it in steps, each with its own TODO:

1. TODO 35, `config/celery.py`: the app. The lesson's section 3 covers it.
2. TODO 36, `config/__init__.py`: load the app with Django. Only do this after step 1 works, or every test in the project fails on import.
3. TODO 37, `config/settings.py`: the Celery settings, the beat schedule and the organiser's address.
4. TODO 38a, `circles/tasks.py`: `current_week`. Check with `pytest circles/tests/test_tasks.py -k week`.
5. TODO 38b, `send_unpaid_report`, then TODO 38c, `queue_unpaid_reports`.

Run the whole file after each step. Some tests stay red until the last step, and that is expected.

## Exit checklist
- [ ] I can name the broker, the worker and beat, and say what each one does
- [ ] I can say why a task takes an ID, not a model object
- [ ] I can name one error that should be retried and one that should not, and say why
- [ ] I can explain how an eager test can pass while production fails
- [ ] `pytest circles/tests/test_tasks.py` passes, all 16 tests
- [ ] (Optional) I started a worker and beat locally and saw one scheduled task run

## Common mistakes
- Queuing a task before the database commit (section 5).
- Passing model objects, which cannot travel to a worker.
- Retrying every exception with `autoretry_for=(Exception,)`, which hides bugs as retries.
- Starting beat without a worker: beat queues the task, and nothing runs it.
- Setting `CELERY_TASK_EAGER_PROPAGATES` to `True`, then wondering why a retry raises `Retry`.
