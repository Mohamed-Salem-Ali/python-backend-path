# Week 2: Functions, modules and the standard library, error handling

Goal by Saturday: write clean reusable functions, use the standard library instead of reinventing it, and handle errors on purpose. You finish with a real tool: the Gameya calculator CLI.

Daily shape: **Learn 1–1.5 h → Build 1–1.5 h → Drill 20 min → Wrap-up 10 min** (see [the plan](../docs/12-week-plan.md)). On a short day (2 h), do Learn and Wrap-up only.

| Day | Learn | Build / exercises | Drill |
|---|---|---|---|
| **1** | [05 Functions](05-functions/lesson.md) part 1: parameters, defaults, `*args/**kwargs`, pass-by-reference | exercises 1–5 | 1 easy problem |
| **2** | 05 part 2: scope (LEGB), first-class functions, closures, recursion | exercises 6–13, finish the file | 1 easy problem |
| **3** | [06 Modules and stdlib](06-modules-packages-stdlib/lesson.md) part 1: imports, packages, `datetime` | exercises 1–5 | 1 easy problem |
| **4** | 06 part 2: `collections`, `itertools`, `functools`, `json`, `pathlib`, `re` | exercises 6–13, finish the file | 1 easy problem |
| **5** | [08 Error handling](08-error-handling/lesson.md) | exercises 1–10 | 1 easy problem |
| **6** | Review | **[Week 2 project](week-2-project/README.md)**, start to finish | 1 problem |
| **Review day** | Redo your weakest exercise from memory | Polish and run the project, commit | Write 2–3 interview questions with your own answers |

## Daily wrap-up
```
Date:
Learned:
Confused by:
Tomorrow:
```

## Checkpoint (end of week)
Without notes you can:
- [ ] Explain why a mutable default argument is a bug and show the fix
- [ ] Write a closure, and explain when `nonlocal` is needed
- [ ] Explain the LEGB rule with an example
- [ ] Use `Counter`, `defaultdict`, `datetime`, `pathlib` and `json` for a task without looking up the basics
- [ ] Explain what `if __name__ == "__main__":` does
- [ ] Write `try/except/else/finally` and say what each part is for
- [ ] Define a custom exception with attributes, and raise one `from` another
- [ ] Write a context manager as a class and with `@contextmanager`
