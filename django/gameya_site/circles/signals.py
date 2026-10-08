"""Signals: react to model events, such as a row being saved or deleted. Module 07."""

from django.db.models.signals import post_delete, post_save  # noqa: F401  (you will use them)
from django.dispatch import receiver  # noqa: F401  (you will use it)

from .models import Member, Payment  # noqa: F401

# Import AuditEntry from .models once TODO 26 exists. Do not import it before then: a failed
# import here breaks every test that imports this module.

# TODO 24: three receivers. Write each one with @receiver(signal, sender=Model), and let it
#          take (sender, instance, **kwargs). The post_save receiver also reads created.
#          a) post_save for Payment, only when created is True. It writes an AuditEntry with
#             action "created".
#          b) post_delete for Payment. It writes an AuditEntry with action "deleted".
#          c) post_delete for Member. It writes an AuditEntry with action "deleted".
#          Each entry stores: model = the lowercase model name ("payment" or "member"),
#          object_id = instance.pk, and summary = str(instance). Store the text now. After a
#          delete the row is gone, so do not build the summary later. Deleting a member also
#          deletes its payments, so those fire (b) too. Payouts and gameyas are not audited.
