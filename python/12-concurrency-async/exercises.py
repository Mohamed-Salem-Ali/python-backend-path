"""Module 12 exercises. Fill the TODOs, run:  python python/12-concurrency-async/exercises.py

The checks count how many calls run at the same time, instead of timing them, so a slow computer
does not make a correct answer fail. Run the file from the repo root.
"""

import asyncio
import multiprocessing
import os
import threading
import time
from concurrent.futures import (  # noqa: F401  (you will need these)
    ProcessPoolExecutor,
    ThreadPoolExecutor,
)

# --- Given: helpers. Read them, do not change them. ------------------------------------------------


class InFlight:
    """Counts the calls that are running at the same time. `peak` is the largest count seen."""

    def __init__(self):
        self.now = 0
        self.peak = 0
        self._lock = threading.Lock()

    def enter(self):
        with self._lock:
            self.now += 1
            self.peak = max(self.peak, self.now)

    def leave(self):
        with self._lock:
            self.now -= 1


def slow_io(name, delay=0.05, tracker=None):
    """Pretend to fetch data. It blocks the calling thread for `delay` seconds."""
    if tracker is not None:
        tracker.enter()
    try:
        time.sleep(delay)
        if name.startswith("bad"):
            raise ValueError(f"cannot fetch {name}")
        return f"data for {name}"
    finally:
        if tracker is not None:
            tracker.leave()


async def slow_io_async(name, delay=0.05, tracker=None):
    """The same fetch as an async function. It waits without blocking the event loop."""
    if tracker is not None:
        tracker.enter()
    try:
        await asyncio.sleep(delay)
        if name.startswith("bad"):
            raise ValueError(f"cannot fetch {name}")
        return f"data for {name}"
    finally:
        if tracker is not None:
            tracker.leave()


class SlowCounter:
    """A counter that is unsafe on purpose. add() reads the value, waits, then writes it back.
    Two threads that call add() at the same time overwrite each other, unless a lock protects
    the call."""

    def __init__(self):
        self.value = 0

    def add(self, amount):
        current = self.value
        time.sleep(0.0005)
        self.value = current + amount


def sum_of_squares(numbers):
    # This function is for worker processes only. Running it in the main process raises an error,
    # so exercise 3 only passes when the work really goes to other processes.
    if multiprocessing.current_process().name == "MainProcess":
        raise RuntimeError("sum_of_squares must run in a worker process")
    return sum(n * n for n in numbers)


def where_am_i(_job):
    """Return the id of the process that runs this function."""
    return os.getpid()


# --- Threads ---------------------------------------------------------------------------------------


# 1. Fetch every name with slow_io, in a pool of `workers` threads (ThreadPoolExecutor with
#    max_workers=workers). Return the results in the same order as `names`. Use the pool's map
#    method. Each call uses a delay of 0.2 seconds and passes `tracker` on to slow_io.
def fetch_in_threads(names, workers, tracker=None):
    # TODO
    ...


# 2. Start `threads` threads. Each one calls counter.add(1) `increments` times. Wrap every call
#    in `with lock:`, so that only one thread updates the counter at a time. Return the final
#    value of the counter. Create the counter and the lock inside the function.
def count_with_lock(threads, increments):
    # TODO
    ...


# --- Processes -------------------------------------------------------------------------------------


# 3. Give each list in `chunks` to sum_of_squares, in a ProcessPoolExecutor. Return the sums in the
#    same order as `chunks`. Use the pool's map method.
def sum_squares_in_processes(chunks):
    # TODO
    ...


# 4. Run where_am_i once for each of `jobs` jobs, in a ProcessPoolExecutor with max_workers=2.
#    Return the list of process ids, one per job. They are the ids of the worker processes.
def worker_pids(jobs):
    # TODO
    ...


# --- asyncio ---------------------------------------------------------------------------------------


# 5. An async function that waits `delay` seconds with asyncio.sleep, then returns x times 2.
#    Use await. time.sleep would block the whole event loop.
async def double_later(x, delay=0.01):
    # TODO
    ...


# 6. Start slow_io_async for every name at once, with asyncio.gather. Use a delay of 0.2 seconds
#    and pass `tracker` on. Return the results in the same order as `names`.
async def fetch_all(names, tracker=None):
    # TODO
    ...


# 7. Start slow_io_async for every name at once, with asyncio.gather and return_exceptions=True.
#    One failure must not stop the others. Return the list of results. A failed name appears in
#    the list as its exception object.
async def fetch_some(names):
    # TODO
    ...


# 8. Call slow_io_async(name, delay) and give up after `seconds` with asyncio.wait_for. On a
#    timeout, return `default`. Otherwise return the result.
async def fetch_or_default(name, delay, seconds, default="none"):
    # TODO
    ...


# 9. Wait 10 seconds with asyncio.sleep. If the task is cancelled, append "cleaned up" to `log`,
#    then raise the CancelledError again, so the task ends as cancelled. Do not swallow the
#    cancellation.
async def sleep_and_clean_up(log):
    # TODO
    ...


# 10. Put every item in an asyncio.Queue. Start `workers` tasks that take items from the queue,
#     wait 0.01 seconds for each one, and add its square to a results list. When the queue is
#     empty, stop the workers. Return the results sorted.
async def process_queue(items, workers):
    # TODO
    ...


# --- Checks ----------------------------------------------------------------------------------------


def check_fetch_in_threads():
    assert fetch_in_threads(["a", "b", "c"], 3) == ["data for a", "data for b", "data for c"]
    tracker = InFlight()
    fetch_in_threads(["a", "b", "c", "d"], 2, tracker)
    assert tracker.peak == 2, f"peak was {tracker.peak}: a pool of 2 threads runs 2 at a time"


def check_count_with_lock():
    assert count_with_lock(8, 20) == 160


def check_sum_squares_in_processes():
    assert sum_squares_in_processes([[1, 2], [3, 4], []]) == [5, 25, 0]


def check_worker_pids():
    pids = worker_pids(4)
    assert len(pids) == 4, pids
    assert os.getpid() not in pids, "the jobs ran in this process, not in worker processes"


def check_double_later():
    assert asyncio.iscoroutinefunction(double_later)
    assert asyncio.run(double_later(4)) == 8

    # While double_later waits, the event loop must keep running other tasks. A time.sleep
    # inside double_later would freeze the ticker, so it would not tick before the wait ends.
    async def scenario():
        ticks = []
        seen_during_wait = []

        async def ticker():
            for _ in range(50):
                ticks.append(1)
                await asyncio.sleep(0.005)

        async def waiter():
            result = await double_later(4, 0.1)
            seen_during_wait.append(len(ticks))
            return result

        result, _ = await asyncio.gather(waiter(), ticker())
        return result, seen_during_wait[0]

    result, ticks_seen = asyncio.run(scenario())
    assert result == 8
    assert ticks_seen >= 5, f"the loop ticked {ticks_seen} times during the wait: do not block it"


def check_fetch_all():
    tracker = InFlight()
    result = asyncio.run(fetch_all(["a", "b", "c", "d"], tracker))
    assert result == ["data for a", "data for b", "data for c", "data for d"], result
    assert tracker.peak == 4, f"peak was {tracker.peak}: gather should start all four at once"


def check_fetch_some():
    result = asyncio.run(fetch_some(["ok", "bad1", "fine"]))
    assert result[0] == "data for ok" and result[2] == "data for fine", result
    assert isinstance(result[1], ValueError) and str(result[1]) == "cannot fetch bad1", result


def check_fetch_or_default():
    assert asyncio.run(fetch_or_default("x", 1.0, 0.05, "late")) == "late"
    assert asyncio.run(fetch_or_default("x", 0.01, 1.0, "late")) == "data for x"


def check_sleep_and_clean_up():
    async def scenario():
        log = []
        task = asyncio.create_task(sleep_and_clean_up(log))
        await asyncio.sleep(0.01)
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            return log
        raise AssertionError("the task finished instead of being cancelled")

    assert asyncio.run(scenario()) == ["cleaned up"]


def check_process_queue():
    # Fed in reverse, so the workers finish out of order: the sort is what makes this pass.
    assert asyncio.run(process_queue([5, 4, 3, 2, 1], 2)) == [1, 4, 9, 16, 25]


if __name__ == "__main__":
    # Run in order, so the first failure points at the first function you have not finished.
    for check in (
        check_fetch_in_threads,
        check_count_with_lock,
        check_sum_squares_in_processes,
        check_worker_pids,
        check_double_later,
        check_fetch_all,
        check_fetch_some,
        check_fetch_or_default,
        check_sleep_and_clean_up,
        check_process_queue,
    ):
        check()
    print("All checks passed")
