"""Admin registrations. Module 03: register the models and shape each admin page."""

from django.contrib import admin  # noqa: F401  (you will use it)

from .models import Gameya, Member, Payment, PayoutSlot  # noqa: F401

# TODO 1: class MemberInline(admin.TabularInline) with model = Member. It shows a gameya's
#         members on the gameya's own page.
# TODO 2: class MemberAdmin(admin.ModelAdmin), registered with @admin.register(Member).
#         Show name, gameya and shares in the list; search by name; filter by gameya.
# TODO 3: class PaymentAdmin(admin.ModelAdmin), registered with @admin.register(Payment).
#         Show member, week, paid_on and amount in the list.
# TODO 4: class GameyaAdmin(admin.ModelAdmin), registered with @admin.register(Gameya).
#         Give it MemberInline in its inlines.
# TODO 5: register PayoutSlot with a ModelAdmin. Show at least turn_number in the list.
