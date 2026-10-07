# Week 3 project: the Gameya domain model

In week 2 you wrote the Gameya rules as loose functions. This week you give them a home: a small set of classes that keep their own data, protect their own rules, and read like Python.

Uses: OOP and dataclasses (07), a generator (09), a decorator (10), and your exceptions from week 2 (08).

## Design

| Piece | What it is |
|---|---|
| `Setup` | A frozen dataclass: `weeks`, `per_week`, `share_value`, `start`. Validates itself, and exposes `turns`, `payout` and `weekly_pot` as properties |
| `Member` | A dataclass: `name`, `shares`. `due(share_value)` is what they pay each week |
| `@audited` | A decorator that logs each successful change to the gameya's `audit_log` |
| `Gameya` | The aggregate: members, payments and turn assignments. It behaves like a collection (`len`, `in`, `for`), reports payment `status`, produces `slots()` lazily, and enforces the per-name turn limit |

## The rules (same as before)

- Payout per turn = `weeks * share_value`; turns = `weeks * per_week`; weekly pot = `turns * share_value`.
- The payment window opens on the Sunday on or before the payout day. Paying before it is an **advance**; paying inside it is **paid**. No payment is **upcoming** until the payout day, then **unpaid**.
- A member can hold at most as many turns as they have shares. With `per_week=2`, turns 1 and 2 are week 1, turns 3 and 4 are week 2, and so on.

## How to work
1. Read `gameya_model.py` top to bottom. Every `TODO` says what to build.
2. Build in this order, running the file as you go: `Setup`, `Member`, then the `Gameya` members, dates, statuses and turns, and last the `audited` decorator. It is already applied to the methods that change data, so until you write it the stub just returns the method unchanged.
3. Run `python python/week-3-project/gameya_model.py`. A pass ends with `All checks passed`.

## Rules for the project
- Standard library only.
- Keep validation inside the classes: it must be impossible to build an invalid `Setup` or break the turn limit through the public methods.
- `slots()` must be a generator, and the audit decorator must not log failed calls.

## Done when
- All checks pass and you can explain why `Setup` is frozen while `Gameya` is not.
- You can explain why `audited` logs after the call, not before.
- Stretch: add `__repr__` to `Gameya`, and a `late(today, week)` method that returns the names of members who are unpaid.
