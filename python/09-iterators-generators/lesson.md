# Module 09: Iterators and generators

By the end you can explain how a `for` loop really works, write your own iterators, and use generators to process data lazily.

## 1. Iterables and iterators
- An **iterable** is anything you can loop over: it has `__iter__`, which returns an iterator (lists, strings, dicts, files, `range`).
- An **iterator** produces values one at a time with `__next__`, and raises `StopIteration` when it is done. An iterator is also iterable (its `__iter__` returns itself).

```python
nums = [10, 20]
it = iter(nums)  # ask the iterable for an iterator
next(it)  # 10
next(it)  # 20
next(it)  # StopIteration
```

A `for` loop is shorthand for exactly that:
```python
it = iter(nums)
while True:
    try:
        item = next(it)
    except StopIteration:
        break
    ...  # the loop body
```
`next(it, default)` returns the default instead of raising.

## 2. Writing an iterator class
```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


list(Countdown(3))  # [3, 2, 1]
```
An iterator is **single-use**: once exhausted it stays exhausted. A new `Countdown(3)` starts over.

## 3. Generators
A function with `yield` is a **generator function**. Calling it does not run the body; it returns a generator object (an iterator). Each `next()` runs until the next `yield`, then pauses with all its local state intact.

```python
def countdown(n):
    while n > 0:
        yield n
        n -= 1


list(countdown(3))  # [3, 2, 1]

g = countdown(2)
next(g)  # 2
next(g)  # 1
next(g)  # StopIteration (the function returned)
```
The same job as the class above, in four lines. A `return` ends the generator.

## 4. Why generators matter: laziness
They compute one value at a time, so they use almost no memory and can be infinite.
```python
def naturals():
    n = 1
    while True:
        yield n
        n += 1


from itertools import islice

list(islice(naturals(), 5))  # [1, 2, 3, 4, 5]

import sys

sys.getsizeof([i * i for i in range(1_000_000)])  # about 8 MB
sys.getsizeof(i * i for i in range(1_000_000))  # about 200 bytes
```
Typical uses: reading a huge file line by line, streaming rows from a database, building pipelines.

## 5. Generator expressions
Like a list comprehension with parentheses; lazy.
```python
total = sum(n * n for n in range(10) if n % 2)  # no intermediate list
any(m["late"] for m in members)  # stops at the first True
```
When a generator expression is the only argument, the extra parentheses are optional.

## 6. `yield from`
Delegate to another iterable.
```python
def flatten(rows):
    for row in rows:
        yield from row  # same as: for x in row: yield x


list(flatten([[1, 2], [3]]))  # [1, 2, 3]
```

## 7. Pipelines
Chain generators so each stage handles one item at a time.
```python
def read_lines(text):
    for line in text.splitlines():
        yield line.strip()


def non_empty(lines):
    for line in lines:
        if line:
            yield line


def to_ints(lines):
    for line in lines:
        yield int(line)


sum(to_ints(non_empty(read_lines("1\n\n2\n3"))))  # 6
```
Nothing runs until `sum` pulls values through the chain.

## 8. Gotchas
- A generator is **exhausted** after one pass. If you need to loop twice, call the function again (or `list()` it first).
- Errors surface when a value is **pulled**, not when the generator is created.
- You can't `len()` or index a generator. Convert with `list()` if you need to.
- `send()`, `throw()` and `close()` let a generator receive values; you will rarely need them yet.

## 9. Handy tools
`enumerate`, `zip`, `map`, `filter` and `reversed` all return lazy iterators. `itertools` adds `chain`, `islice`, `cycle`, `count`, `takewhile`, `groupby`, `pairwise` (3.10+) and more.

## Check your understanding
1. What is the difference between an iterable and an iterator?
2. What does a `for` loop do under the hood?
3. What happens when you call a generator function? When does its body run?
4. Why can a generator handle a 10 GB file but a list cannot?
5. What does `yield from` do?
6. Why does looping twice over the same generator give an empty second pass?

Then do `exercises.py`.
