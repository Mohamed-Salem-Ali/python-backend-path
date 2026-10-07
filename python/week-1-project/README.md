# Week 1 project: contacts and word counter

Uses everything from modules 01–04: variables, strings, lists, dicts, sets, loops, functions, and comprehensions.

## Part A: word counter (`word_counter.py`)
Write `count_words(text) -> dict` returning how often each word appears, ignoring case and punctuation, then `top_words(counts, n) -> list` returning the `n` most common as `(word, count)` tuples (ties in alphabetical order).

```text
"The cat and the hat. The end!"  ->  the: 3, cat: 1, and: 1, hat: 1, end: 1
```

## Part B: contacts book (`contacts.py`)
A list of dicts, each `{"name": ..., "phone": ..., "tags": [...]}`:
1. `add_contact(book, name, phone, tags=())`: reject duplicate names (return `False`), else append (return `True`)
2. `find(book, text)`: contacts whose name contains `text`, case-insensitive
3. `by_tag(book)`: dict mapping each tag to the list of names that have it
4. `format_contact(c)`: one line like `Mohamed | 0100... | family, friend`
5. A small menu loop (`while True`) with: add, search, list, quit

## Rules
- Pure functions first (no `input()` inside them), then a `main()` that does the I/O.
- No imports besides the standard library.
- Run `python word_counter.py` and `python contacts.py`; every function has an `assert` check in the `__main__` block.

## Done when
- Both files run with `All checks passed` and the menu works.
- You can explain every line to a friend.
