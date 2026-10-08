"""Forms: validated input. Module 03."""

from django import forms  # noqa: F401  (you will use it)

from .models import Payment  # noqa: F401

# TODO 1: class PaymentForm(forms.ModelForm). Its Meta uses model = Payment and the fields
#         member, week, paid_on and amount. Its clean() rejects an amount below the
#         member's due() for one week. Use cleaned_data, and handle a missing member.
#         If test_a_missing_member_is_reported_and_does_not_crash fails with an error from
#         models.py, the cause is Payment.clean() there, not this form. Fix it too.
# TODO 2: class JoinForm(forms.Form), a plain form, not tied to a model. It has:
#         name: required text, at most 80 characters, with spaces stripped.
#               The name "admin" is reserved, in any letter case.
#         shares: a whole number from 1 to 5
