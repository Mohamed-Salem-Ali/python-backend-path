# Python syllabus

Weeks 1–4 of the [12-week plan](../docs/12-week-plan.md) (module 12 lands in week 10). Each module has a `lesson.md` and a way to check your work: an `exercises.py` that checks itself, or, in module 13, a test file you write and a checker that grades it.

**Level target:** write, test, package and debug a small Python program on your own, and explain how the language works underneath.

## Core track

| # | Module | You can… | Week |
|---|---|---|---|
| 01 | Environment and tooling | create a venv, install packages, run scripts and the REPL, read a traceback | 1 |
| 02 | Syntax and data types | explain names vs objects, numbers, strings, slicing, truthiness, `==` vs `is` | 1 |
| 03 | Collections | choose between list, tuple, dict and set, and explain mutability and aliasing | 1 |
| 04 | Control flow | write `if`, `for`, `while`, `break/continue/else` and comprehensions | 1 |
| 05 | Functions | use args, kwargs, defaults, scope (LEGB), closures, lambdas, recursion | 2 |
| 06 | Modules, packages, stdlib | structure code into modules; use `os`, `pathlib`, `json`, `datetime`, `collections`, `itertools`, `functools`, `re` | 2 |
| 08 | Error handling | use `try/except/else/finally`, raise and define exceptions, write context managers | 2 |
| 07 | OOP | build classes with inheritance, MRO, dunder methods, properties, composition | 3 |
| 09 | Iterators and generators | explain the iterator protocol and write generators | 3 |
| 10 | Decorators | write decorators with and without arguments, use `functools.wraps` | 3 |
| 11 | Typing | annotate code, use `typing`, run mypy or pyright | 4 |
| 13 | Testing | write pytest tests with fixtures, parametrize and mocking | 4 |
| 14 | Packaging | manage dependencies, `pyproject.toml`, build a package | 4 |
| 15 | Capstone | build a Task Tracker CLI with tests, types and packaging | 4 |
| 12 | Concurrency and async | choose between threads, processes and asyncio; write async/await code | 10 |

## Projects
| Week | Project |
|---|---|
| 1 | [Contacts and word counter](week-1-project/README.md) |
| 2 | [Gameya calculator CLI](week-2-project/README.md): payout, due amounts, pay-window logic as pure functions, with `argparse` and custom exceptions |
| 3 | [Gameya domain model](week-3-project/README.md): dataclasses, a collection-like class, a generator and an audit decorator |
| 4 | [Task Tracker CLI (capstone)](15-capstone-task-tracker/README.md): data model, JSON storage, `argparse` CLI, tests, types and packaging; acceptance tests included |

## Exit exam: "I know Python"
Pass all of these without notes:
- [ ] Explain what happens, step by step, when you run `a = b = []` and then `a.append(1)`
- [ ] Explain closures, generators and decorators, each with a small example from memory
- [ ] Write a context manager two ways (class and `contextlib`)
- [ ] Explain the MRO and what `super()` actually does
- [ ] Write a pytest suite with a fixture and a parametrized test for a function you wrote
- [ ] Explain the GIL and when to use threads, processes or asyncio
- [ ] Package a small tool so it installs with `pip install .` and has a console command
- [ ] Solve 30 easy and 10 medium coding problems

## Advanced tier (after week 12)
For going from good to excellent:
- Python data model in depth: descriptors, `__slots__`, metaclasses (what and when not to)
- Memory and performance: profiling, `timeit`, `cProfile`, generators vs lists, `lru_cache`
- Concurrency in practice: `concurrent.futures`, `asyncio.gather`, task groups, cancellation
- Design: dataclasses, protocols, dependency injection, SOLID in Python
- Tooling: pre-commit, `uv`, `ruff`, `mypy --strict`, CI
- Read real code: the standard library (`collections`, `pathlib`) and one popular small library
