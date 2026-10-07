# Week 3: Classes, generators and decorators

Goal by Saturday: model a problem with classes, process data lazily with generators, and wrap behaviour with decorators. You finish with the Gameya domain model, the same rules as week 2, now as objects.

Daily shape: **Learn 1–1.5 h → Build 1–1.5 h → Drill 20 min → Wrap-up 10 min** (see [the plan](../docs/12-week-plan.md)). On a short day (2 h), do Learn and Wrap-up only.

| Day | Learn | Build / exercises | Drill |
|---|---|---|---|
| **1** | [07 OOP](07-oop/lesson.md) part 1: classes, `__init__`, attributes, `__repr__`, `__eq__`, properties | exercises 1–3 | 1 easy problem |
| **2** | 07 part 2: dunder methods, `classmethod`/`staticmethod`, inheritance, `super()`, MRO, dataclasses | exercises 4–13, finish the file | 1 easy problem |
| **3** | [09 Iterators and generators](09-iterators-generators/lesson.md) | all 12 exercises | 1 easy problem |
| **4** | [10 Decorators](10-decorators/lesson.md) part 1: the idea, `wraps`, wrappers with state | exercises 1–3 (shout, log_calls, count_calls) | 1 easy problem |
| **5** | 10 part 2: factories (`@repeat(3)`), stacking, real patterns | exercises 4–11 | 1 easy problem |
| **6** | Review | **[Week 3 project](week-3-project/README.md)**, start to finish | 1 problem |
| **Review day** | Redo your weakest exercise from memory | Polish and run the project, commit | Write 2–3 interview questions with your own answers |

(The decorator checks run in order, so the error always points at the first decorator you have not finished.)

## Daily wrap-up
```
Date:
Learned:
Confused by:
Tomorrow:
```

## Checkpoint (end of week)
Without notes you can:
- [ ] Explain `self`, instance vs class attributes, and why `__repr__` matters
- [ ] Explain `__eq__` and `__hash__` and when objects are hashable
- [ ] Use a property for validation and a read-only value
- [ ] Explain inheritance, `super()`, polymorphism and the MRO of a diamond
- [ ] Choose between inheritance and composition for a small design
- [ ] Say what `@dataclass` generates, and why a list default needs `default_factory`
- [ ] Explain iterable vs iterator, and what a `for` loop does under the hood
- [ ] Write a generator, a generator expression and a small lazy pipeline
- [ ] Write a decorator with `functools.wraps`, and one with arguments (three layers)
