# Week 2 project: Gameya calculator CLI

A *gameya* (جمعية) is a rotating savings circle: a group pays a fixed amount every week, and each week one person (or two) receives the whole pot. This week you write the money and date rules as **pure functions**, validate them with your own exceptions, and wrap them in a small command-line tool.

Uses: functions (05), `datetime`, `argparse` and `json` (06), and custom exceptions (08).

## The rules

- A gameya has `weeks` weeks, `per_week` payouts each week, and a `share_value` paid per name each week.
- Total turns = `weeks * per_week`.
- Payout per turn = `weeks * share_value` (each name pays every week and receives once).
- Weekly pot = `turns * share_value`.
- Week N starts on the start date plus `7 * (N - 1)` days. Payout day is that date.
- Members pay in a window that **opens on the Sunday on or before the payout day**. A payment made inside the window (up to the payout day) is on time. A payment made before the window is an **advance** payment.
- A week with no payment is **upcoming** until its payout day arrives, then **unpaid**.

## Part A: the rules (`gameya_calc.py`)
Fill in the functions. The `__main__` block checks them.

| Function | Returns |
|---|---|
| `turns(weeks, per_week)` | total number of turns |
| `payout(weeks, share_value)` | amount received per turn |
| `weekly_pot(weeks, per_week, share_value)` | money collected each week |
| `week_start(start, week)` | ISO date of that week's payout day |
| `pay_window_start(start, week)` | ISO date the window opens (Sunday on or before) |
| `status(start, week, today, paid_on=None)` | `"paid"`, `"advance"`, `"unpaid"` or `"upcoming"` |
| `validate_setup(weeks, per_week, share_value)` | raises `InvalidSetup` when any number is not a positive integer |
| `summary(weeks, per_week, share_value, start)` | a dict with the figures and the schedule |

## Part B: the command line
`main(argv)` uses `argparse`:

```bash
python python/week-2-project/gameya_calc.py --weeks 10 --per-week 2 --share 100 --start 2026-10-10
python python/week-2-project/gameya_calc.py --weeks 10 --per-week 2 --share 100 --start 2026-10-10 --json
```

- Without `--json`, print a readable summary.
- With `--json`, print the `summary` dict as JSON.
- On `InvalidSetup`, print the message to standard error and return exit code `2` (don't show a traceback).

## Rules for the project
- Standard library only.
- Pure functions first; I/O only in `main`.
- Make the checks in the `__main__` block pass before you touch the CLI.

## Done when
- `All checks passed` prints, and the CLI works with and without `--json`.
- You can explain why `payout` does not depend on the number of members.
