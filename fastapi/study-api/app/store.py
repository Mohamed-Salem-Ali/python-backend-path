"""Where summaries are kept for now: a dict in memory. The database comes later in this track.

Each record is a dict. It has an "owner" field that the API must never send back, so the routes
use response models to leave it out.
"""

SUMMARIES: dict[int, dict] = {}
_last_id = [0]


def next_id() -> int:
    _last_id[0] += 1
    return _last_id[0]


def reset() -> None:
    SUMMARIES.clear()
    _last_id[0] = 0
