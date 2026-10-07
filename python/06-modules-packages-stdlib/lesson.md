# Module 06: Modules, packages and the standard library

By the end you can split code into modules and packages, and reach for the right standard-library tool instead of writing it yourself.

## 1. Modules
Any `.py` file is a **module**. Importing runs it once and gives you its names.
```python
import math  # math.sqrt(9)
from math import sqrt, pi  # sqrt(9)
from math import sqrt as root  # alias
import datetime as dt  # common alias
```
- Prefer `import module` or specific names. Avoid `from module import *` (it hides where names come from).
- Python looks for a module in: the current script's folder, then `sys.path` (installed packages, the standard library). Inspect it with `import sys; sys.path`.
- Do not name your file the same as a library (`random.py`, `json.py`): yours would shadow the real one.

### The `__main__` guard
```python
def main(): ...


if __name__ == "__main__":  # true only when run directly, not when imported
    main()
```
That is why every `exercises.py` can run its checks without running them on import.

## 2. Packages
A **package** is a folder of modules. A folder with an `__init__.py` is a regular package.
```text
gameya/
    __init__.py
    schedule.py
    money.py
```
```python
from gameya import schedule
from gameya.money import due_amount
```
Inside a package, relative imports say "from my own package": `from .money import due_amount`. Run packages with `python -m gameya.schedule` so imports resolve.

## 3. A tour of the standard library
Python ships with a large library. Learn what exists so you do not reinvent it. Read the official docs for each; here are the ones you will use constantly.

### `datetime`: dates and times
```python
from datetime import date, datetime, timedelta

d = date(2026, 10, 10)
d.weekday()  # 0 = Monday ... 5 = Saturday, 6 = Sunday
d + timedelta(days=7)  # next week
date.fromisoformat("2026-10-10")  # parse
d.isoformat()  # '2026-10-10'
(date(2026, 10, 17) - d).days  # 7
d.strftime("%A %d %B %Y")  # 'Saturday 10 October 2026'
```
Use ISO strings (`YYYY-MM-DD`) when storing or passing dates around.

### `collections`
```python
from collections import Counter, defaultdict, deque, namedtuple

Counter("banana").most_common(2)  # [('a', 3), ('n', 2)]
groups = defaultdict(list)
groups["a"].append(1)
q = deque([1, 2])
q.appendleft(0)
q.pop()
Point = namedtuple("Point", "x y")
```

### `itertools` and `functools`
```python
from itertools import chain, islice, accumulate, groupby, product, combinations

list(accumulate([1, 2, 3]))  # [1, 3, 6]
list(chain([1], [2, 3]))  # [1, 2, 3]
list(islice(range(100), 3))  # [0, 1, 2]
list(combinations("abc", 2))

from functools import lru_cache, partial, reduce


@lru_cache(maxsize=None)  # memoize a pure function
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


hex2 = partial(int, base=16)  # fix an argument
```

### `json`
```python
import json

text = json.dumps({"name": "جمعية", "n": 1}, ensure_ascii=False, sort_keys=True, indent=2)
data = json.loads(text)
```
`dumps`/`loads` work with strings; `dump`/`load` with files.

### `pathlib`: files and folders
```python
from pathlib import Path

p = Path("notes") / "day1.txt"  # build paths with /
p.parent.mkdir(parents=True, exist_ok=True)
p.write_text("hello\n", encoding="utf-8")
p.read_text(encoding="utf-8")
p.exists(), p.suffix, p.stem, p.name
for f in Path(".").glob("*.py"):
    ...
```
Always pass `encoding="utf-8"` when reading or writing text.

### `re`: regular expressions (basics)
```python
import re

re.findall(r"\d+", "weeks 10 and 12")  # ['10', '12']
m = re.search(r"(\w+)@(\w+)\.com", "ali@example.com")
m.group(1)  # 'ali'
re.sub(r"\s+", " ", "a   b")  # 'a b'
```
Use raw strings (`r"..."`) for patterns.

### Others to know exist
`os` and `sys` (environment, arguments), `argparse` (command-line options), `random`, `math`, `statistics`, `csv`, `logging`, `textwrap`, `tempfile`, `shutil`, `decimal` and `fractions`.

## 4. Third-party vs standard library
`pip install` brings in packages from PyPI. Use the standard library when it does the job; add a dependency only when it earns its place.

## Check your understanding
1. What happens when you `import` a module twice?
2. What does `if __name__ == "__main__":` do, and why use it?
3. What makes a folder a package, and how do relative imports differ from absolute ones?
4. Which tool counts words, which groups values into lists, and which caches a function's results?
5. How do you add 7 days to a date and get the weekday name?
6. Why use `pathlib` instead of joining strings with `/`?
7. Why pass `ensure_ascii=False` when dumping Arabic text to JSON?

Then do `exercises.py`.
