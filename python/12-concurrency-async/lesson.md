# Module 12: Concurrency and async

By the end you can tell which kind of waiting a program does, choose threads, processes or asyncio for it, write `async`/`await` code, and keep shared state safe.

**Before you start:** finish modules 05 (functions), 08 (error handling) and 09 (generators). Use Python 3.11 or newer; the examples use `asyncio` features from 3.11. This course uses 3.12.

**Setup:** nothing new to install. Everything comes with the standard library. Run the exercises from the repo root:

```bash
python python/12-concurrency-async/exercises.py
```

A passing file prints `All checks passed`. The checks count how many calls run at the same time, instead of timing them. A slow computer does not make a correct answer fail.

**How to read the examples:** the examples use made-up functions such as `fetch_page` and `resize_photo`. They are not the exercises. Learn the pattern, then solve the exercises.

## 1. Two kinds of work
Think about what a program waits for.

- **I/O-bound** work waits for something outside the processor: a network reply, a file, a database. The processor is idle during the wait.
- **CPU-bound** work keeps the processor busy: parsing, resizing an image, adding up a long list.

A program with five network calls that take one second each needs five seconds if it makes them one after another. If it starts all five first and waits for them together, it needs about one second. That is the gain from concurrency, and it only helps when the work waits. For CPU-bound work, the gain comes from running on several cores, which is a different tool.

```python
import time


def fetch_page(url):
    time.sleep(1)  # stands in for a network call
    return f"page {url}"


start = time.perf_counter()
pages = [fetch_page(url) for url in ["a", "b", "c"]]
print(round(time.perf_counter() - start))  # 3: one after another
```

## 2. The GIL, in one paragraph
CPython, the standard Python, has a global interpreter lock, the GIL. Only one thread runs Python bytecode at a time. A thread gives up the GIL while it waits on I/O, so other threads can run during the wait. That is why threads help with I/O-bound work and do not speed up CPU-bound work. Each process has its own interpreter and its own GIL, so processes can use several cores. Recent Python versions include an experimental build without the GIL; the default build used in this course still has it.

## 3. Threads for waiting
A thread runs a function on its own, while the main program keeps going. `concurrent.futures.ThreadPoolExecutor` manages a pool of them:

```python
from concurrent.futures import ThreadPoolExecutor


def fetch_page(url):
    time.sleep(1)
    return f"page {url}"


with ThreadPoolExecutor(max_workers=3) as pool:
    pages = list(pool.map(fetch_page, ["a", "b", "c"]))  # about 1 second, in input order
```

`map` returns results in the order of the input, even when the calls finish in another order. `max_workers` caps how many run at once.

Threads share memory, and that makes races possible. This function has a race: two threads can read the same value before either writes it back.

```python
counter = {"value": 0}


def add_one():
    current = counter["value"]
    time.sleep(0.0005)  # a moment when another thread can run
    counter["value"] = current + 1
```

A `threading.Lock` lets one thread at a time run the risky part:

```python
import threading

lock = threading.Lock()


def add_one():
    with lock:
        current = counter["value"]
        time.sleep(0.0005)
        counter["value"] = current + 1
```

Keep the lock as short as you can, and never wait for another thread while you hold it.

**Try it:** run the racy version with eight threads, each adding one twenty times. Then add the lock and run it again. Compare the two totals.

## 4. Processes for CPU work
A process has its own interpreter and its own GIL, so `ProcessPoolExecutor` can use several cores:

```python
from concurrent.futures import ProcessPoolExecutor


def resize_photo(path):
    # imagine heavy pixel work here
    return sum(i * i for i in range(10_000_000))


if __name__ == "__main__":
    with ProcessPoolExecutor() as pool:
        sizes = list(pool.map(resize_photo, ["a.jpg", "b.jpg"]))
```

Three rules:

- The function you send must be defined at the top level of a module, so the other process can import it. A lambda or a function inside another function cannot be sent.
- Put the start of your program under `if __name__ == "__main__":`. On Windows and macOS, a new process imports your module again. Without the guard, each new process would start more processes.
- Data travels between processes as copies. Sending a big list costs time, and so does starting a process. Use processes for work that takes long enough to pay for both.

**Try it:** print `os.getpid()` inside the function, and again in the main program. The numbers differ. Then replace `ProcessPoolExecutor` with `ThreadPoolExecutor` and see the numbers become one.

## 5. asyncio: one thread, many waits
An `async def` function is a coroutine. Calling it does not run it; it returns a coroutine object. `await` runs it, and while it waits, the event loop runs other coroutines:

```python
import asyncio


async def fetch_page(url):
    await asyncio.sleep(1)  # waits without blocking the event loop
    return f"page {url}"


async def main():
    page = await fetch_page("a")
    print(page)


asyncio.run(main())  # starts the event loop, runs main, and closes the loop
```

The rule that causes most bugs: never call a blocking function inside `async def`. `time.sleep(1)` in that function freezes the whole event loop for a second, and nothing else runs. Use `asyncio.sleep`, or an async library, and move blocking work to a thread with `asyncio.to_thread`.

Forgetting `await` is the other common bug. `fetch_page("a")` without `await` creates a coroutine that never runs. Python warns with "coroutine was never awaited".

**Try it:** write a function that calls `time.sleep(1)` inside `async def`, and start two of them with `asyncio.gather`. Measure how long they take. Then change it to `await asyncio.sleep(1)` and measure again.

## 6. Running many at once
`asyncio.gather` starts several coroutines and returns their results in input order:

```python
async def main():
    pages = await asyncio.gather(fetch_page("a"), fetch_page("b"), fetch_page("c"))
```

By default, the first exception stops the gather and reaches the caller. With `return_exceptions=True`, each failure is returned in the list as its exception object, and the other coroutines keep running. Choose it when partial results are useful.

`asyncio.TaskGroup` (3.11 and newer) is the stricter version: when one task fails, the group cancels the rest, and the error comes out of the `async with` block:

```python
async with asyncio.TaskGroup() as group:
    first = group.create_task(fetch_page("a"))
    second = group.create_task(fetch_page("b"))
print(first.result(), second.result())
```

To give up after a time, use `asyncio.wait_for(coroutine, timeout=seconds)`. On a timeout it cancels the coroutine and raises `TimeoutError`.

## 7. Cancellation
`task.cancel()` does not kill a task at once. It raises `asyncio.CancelledError` at the task's next `await`. The task can clean up, and it must then raise the error again, so the task really ends as cancelled:

```python
async def download(log):
    try:
        await asyncio.sleep(60)
    except asyncio.CancelledError:
        log.append("closed the file")
        raise
```

If you catch `CancelledError` and do not raise it again, the task looks like it finished normally, and the code that cancelled it cannot tell. `CancelledError` is a `BaseException`, not an `Exception`, so a plain `except Exception` does not catch it.

## 8. Queues: a line of work
`asyncio.Queue` connects a producer, which adds work, to workers, which take it out. A worker calls `get()`, does the work, then calls `task_done()`. The producer can wait on `queue.join()`, which returns once every item has been marked done:

```python
async def worker(queue, results):
    while True:
        item = await queue.get()
        try:
            results.append(await handle(item))
        finally:
            queue.task_done()  # without this, join() waits forever
```

If a script hangs at `join()`, look for a `get()` without a matching `task_done()`.

## 9. Choosing
| The work is | Use | Why |
|---|---|---|
| waiting on many network calls, and the libraries are async | asyncio | one thread handles thousands of waits |
| waiting on calls from a library that blocks | threads (`ThreadPoolExecutor`) | the GIL is released during the wait |
| heavy computation on the processor | processes (`ProcessPoolExecutor`) | each process has its own GIL and core |
| a small script with one or two slow calls | plain code | concurrency adds complexity you do not need |

## 10. Common mistakes
- `time.sleep` or a blocking library call inside `async def`. It freezes every other task.
- An `await` left out, so the coroutine never runs.
- A `CancelledError` caught and not raised again.
- Threads that update shared data without a lock.
- A process pool without the `if __name__ == "__main__":` guard, or with a lambda as the function.
- A queue `get()` without `task_done()`, so `join()` never returns.
- Tasks created without keeping a reference to them, so their result or error is lost.
