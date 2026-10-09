"""Caching: build a gameya's summary once, keep it in the cache, and clear it when the data changes.
Module 09.

The cache is shared by the whole process, so the tests empty it before each test (see
circles/tests/test_performance.py).
"""

from django.core.cache import cache  # noqa: F401  (you will use it)

from .models import Gameya  # noqa: F401  (you will use it)


# TODO 31: build_summary(gameya_id) -> dict, with at most 3 queries however many members there are.
#          Load the gameya, its members and each member's payments in a fixed number of queries,
#          so that the number does not grow with the members. Ask the database for the gameya
#          with its members and their payments loaded in batches (read about prefetch_related).
#          Return:
#            {"name": the gameya's name,
#             "collected": the total of every payment in the gameya (0 when there are none),
#             "members": [{"name": ..., "due": member.due(), "paid": the total of that member's
#                          payments (0 when none)}, ...]}
#          The members come in their default order. A missing gameya raises Gameya.DoesNotExist.
#          Sum the prefetched payments in Python: do not query inside the loop.
def build_summary(gameya_id):
    """The summary of one gameya, built with at most 3 queries."""
    ...


# TODO 32: gameya_summary(gameya_id) -> dict. Return the summary stored under the key
#          f"gameya:{gameya_id}:summary". On a miss, call build_summary, store the result under
#          that key with the cache's default timeout, and return it. A cache hit runs no queries.
def gameya_summary(gameya_id):
    """The cached summary of one gameya; builds and stores it on a miss."""
    ...


# TODO 33: invalidate_summary(gameya_id) deletes the key from TODO 32, so the next call rebuilds
#          the summary. Then clear it on every change: signals.py gets the receivers (see TODO 33
#          there). Do not clear the whole cache: other gameyas keep theirs.
def invalidate_summary(gameya_id):
    """Remove the cached summary of one gameya."""
    ...
