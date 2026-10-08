"""Shared fixtures for the pytest tests in this folder. Module 08.

pytest finds these fixtures by name in every test file in circles/tests/. A test asks for a
fixture by putting its name in the test's arguments. A fixture that writes to the database must
take the built-in db fixture, or pytest-django refuses the write.
"""

import pytest  # noqa: F401  (you will use it)
from rest_framework.authtoken.models import Token  # noqa: F401  (you will use it)
from rest_framework.test import APIClient  # noqa: F401  (you will use it)

from circles.tests import factories as circle_factories  # noqa: F401

PASSWORD = "test-only-password-123"

# TODO 30: write these fixtures. Each one is a function decorated with @pytest.fixture.
#   gameya(db)                       -> one saved gameya, built by circle_factories.GameyaFactory.
#   staff_user(django_user_model)    -> a superuser with the password PASSWORD. The user model's
#                                       manager has a method for making superusers, the one the
#                                       createsuperuser command uses. Take the db fixture too.
#                                       A superuser has every permission, and the admin page
#                                       checks them.
#   reader_user(django_user_model)   -> a user who is not staff, with the same password.
#   staff_token(staff_user)          -> a saved Token for staff_user. Token is imported above.
#   reader_token(reader_user)        -> a saved Token for reader_user.
#   staff_client(client, staff_user) -> the test client, logged in as staff_user without a
#                                       password. The test client has a method for this.
#   api_client()                     -> an APIClient with no login. APIClient is imported above.
#
# Use the names exactly as written: the tests ask for them by name.
