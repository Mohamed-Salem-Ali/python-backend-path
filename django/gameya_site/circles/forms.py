"""Forms: validated input. Module 03."""

from django import forms  # noqa: F401  (you will use it)

from .models import Member, Payment  # noqa: F401

# TODO 1: class PaymentForm(forms.ModelForm). Its Meta uses model = Payment and the fields
#         member, week, paid_on and amount. Its clean() rejects an amount below the
#         member's due() for one week. Use cleaned_data, and handle a missing member.
# TODO 2: class JoinForm(forms.Form), a plain form, not tied to a model. It has:
#         name: required text, at most 80 characters, with spaces stripped
#         shares: a whole number from 1 to 5
