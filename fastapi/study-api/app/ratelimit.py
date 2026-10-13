"""Rate limits: how many requests one caller may make in a minute.

Module 13 (a real model and rate limits): fill in the TODOs. Read the lesson, sections 6 to 8.

The limiter keeps its counts in this process's memory. That is enough for one server process.
With several processes, each one would count on its own, and section 8 says what to use instead.
"""

import math  # noqa: F401  (you will use it)
import time

from app.config import get_settings  # noqa: F401  (you will use it)
from app.dependencies import get_optional_user  # noqa: F401  (you will use it)
from fastapi import Depends, HTTPException, Request  # noqa: F401  (you will use these)


# TODO 34: RateLimiter(limit, window_seconds=60, clock=time.monotonic) counts hits per key in a
#          sliding window. Keep, for each key, the times of its recent hits (a deque from
#          collections works well). Lesson, section 6.
#          hit(key) records a hit and returns None when the key is under its limit. When the key
#          already has `limit` hits in the last window_seconds, it records nothing and returns
#          the number of seconds until the oldest of them leaves the window. Drop hits that are
#          window_seconds old or older before you count. A limit of 0 means no limit: hit()
#          always returns None. Read the time from self.clock(), never from time directly, so
#          a test can move the clock by hand.
class RateLimiter:
    def __init__(self, limit, window_seconds=60, clock=time.monotonic):
        raise NotImplementedError("TODO 34")

    def hit(self, key):
        raise NotImplementedError("TODO 34")


# TODO 34: get_rate_limiter() returns one RateLimiter for the whole process, with the limit from
#          get_settings().rate_limit_per_minute. Build it on the first call and return the same
#          one after that: functools.cache does this. Tests replace it with a dependency
#          override. Lesson, section 7.
def get_rate_limiter():
    raise NotImplementedError("TODO 34")


# TODO 34: rate_limit(request, limiter, user) is the dependency the routes use. It takes
#          request: Request, limiter from Depends(get_rate_limiter), and user from
#          Depends(get_optional_user). The key names the route and the caller: the method and the
#          path, then "user:<id>" for a signed-in user or "ip:<address>" (request.client.host)
#          for everyone else. When hit() returns a wait, raise HTTPException 429 with the detail
#          "too many requests" and the header Retry-After: the wait in whole seconds, rounded
#          up. Lesson, section 7.
async def rate_limit():
    raise NotImplementedError("TODO 34")
