# Week 4: Typing, testing, packaging and the capstone

Goal by Saturday: write typed, tested, installable Python, and ship the **Task Tracker CLI**. This is the last week of the Python phase; Django starts next.

Daily shape: **Learn 1–1.5 h → Build 1–1.5 h → Drill 20 min → Wrap-up 10 min** (see [the plan](../docs/12-week-plan.md)). On a short day (2 h), do Learn and Wrap-up only. This week has the most building, so protect the Build block.

| Day | Learn | Build / exercises | Drill |
|---|---|---|---|
| **1** | [11 Typing](11-typing/lesson.md) | exercises 1–6 | 1 easy problem |
| **2** | 11 part 2: `TypedDict`, `Protocol`, generics, `Literal`; run `mypy` | exercises 7–12, then `mypy exercises.py` | 1 easy problem |
| **3** | [13 Testing](13-testing/lesson.md): pytest, parametrize, fixtures | tests 1–5 in `test_payments.py` | 1 problem |
| **4** | 13 part 2: `tmp_path`, `monkeypatch`, mocks, mutation checks | tests 6–10, then `python python/13-testing/check_tests.py` until every bug is caught | 1 problem |
| **5** | [14 Packaging](14-packaging/lesson.md) | finish `gameya_toolkit`, `exercises.py`, `pip install -e` | 1 problem |
| **6** | [15 Capstone](15-capstone-task-tracker/README.md): read the spec and the acceptance tests | build `models`, `storage`, then the CLI commands | 1 problem |
| **Review day** | Finish the capstone: own tests, `mypy --strict`, `ruff`, install and use it | Commit; write the capstone's own README | Write 2–3 interview questions with your own answers |

The capstone is about two days of work. If you run short, finish the acceptance tests first and spread the rest (your own tests, `mypy`, README) over the next days before starting Django. It is better to finish it than to start Week 5 half done.

## Daily wrap-up
```
Date:
Learned:
Confused by:
Tomorrow:
```

## Checkpoint (end of week)
Without notes you can:
- [ ] Annotate functions with unions, `Sequence`, `Callable`, and explain why you accept abstract types
- [ ] Describe a dict's shape with `TypedDict`, and duck-typed objects with a `Protocol`
- [ ] Write a generic function and a generic class
- [ ] Write parametrized tests, fixtures, a `tmp_path` test, a `monkeypatch` test and a `Mock` assertion
- [ ] Explain why 100% coverage is not enough, and what a mutation check adds
- [ ] Write a `pyproject.toml` with metadata, dependencies and a console script
- [ ] Install a package in editable mode and build a wheel
- [ ] Design a small program with a clear model, storage and CLI layer, and turn errors into exit codes in one place

## Phase 0 exit exam
Before you start Django, go through the [Python exit exam](SYLLABUS.md#exit-exam-i-know-python). Anything you cannot do without notes goes on your list for the Day 6 review.
