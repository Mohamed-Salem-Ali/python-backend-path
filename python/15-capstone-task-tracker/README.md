# Capstone: Task Tracker CLI

Everything from the Python phase in one program: data modelling, validation, files, errors, a command line, type hints, tests and packaging. When this passes, you have finished the Python track.

```bash
pip install -e ".[dev]"        # from this folder, inside a virtual environment
tasks add "Buy milk" --priority high --due 2026-10-20
tasks list
tasks done 1
tasks stats
```

## What it must do

Global options (before the command): `--file PATH` (default `tasks.json`) and `--today YYYY-MM-DD` (default: today; it makes "overdue" testable).

| Command | Behaviour | Output |
|---|---|---|
| `add TITLE [--priority high\|normal\|low] [--due YYYY-MM-DD]` | Creates a task. Priority defaults to `normal`. | `Added #1: Buy milk` |
| `list [--all]` | Open tasks only, or every task with `--all` | One line per task, or `No tasks.` |
| `done ID` | Marks a task done | `Completed #1` |
| `remove ID` | Deletes a task | `Removed #1` |
| `stats` | Counts | `open: 3, done: 1, overdue: 1` |

**List line format** (two spaces before `due`, which appears only when there is a due date):
```text
#1 [ ] (high) Buy milk  due 2026-10-20
#2 [x] (normal) Call Sara
```
**Order:** high priority first, then earlier due date (no date goes last), then lower id.
**Overdue:** an open task whose due date is before `--today`. Due today is not overdue; done tasks are never overdue.

**Rules**
- Titles are trimmed and must be 1–80 characters. Priority must be one of the three. A due date must be a real calendar date.
- Ids start at 1, always increase, and are **never reused**, even after a removal.
- Data lives in one JSON file: `{"next_id": 3, "tasks": [{"id": 1, "title": "...", "done": false, "priority": "normal", "due": null, "created": "2026-10-10"}]}`. UTF-8, so Arabic titles work. A missing file means no tasks yet.

**Errors** go to standard error, nothing to standard output:

| Situation | Exit code | Message includes |
|---|---|---|
| Unknown task id | `1` | `No task #9` |
| Tasks file is not valid JSON or has the wrong shape | `1` | `error` |
| Bad title or due date | `2` | `error:` and the word `title` or `due` |
| Bad priority or unknown option | `2` | argparse's usage message |

## The acceptance tests are your target

`tests/test_acceptance.py` already contains the tests for everything above. They use only the command line, so how you build the inside is your design. Run them from this folder:

```bash
pytest                  # all fail at first; make them pass one at a time
pytest -x -q            # stop at the first failure
```
Do not edit `test_acceptance.py`.

## Suggested design

- `models.py`: a `Task` dataclass that validates itself in `__post_init__`; exceptions that tell the caller what kind of problem it is (`ValidationError`, `NotFound`, `StorageError`).
- `storage.py`: `load(path)` and `save(path, next_id, tasks)`. Nothing else touches the file.
- `cli.py`: parse arguments with `argparse` sub-commands, call the pieces, print, and turn exceptions into exit codes in **one** place.
- Keep functions small and pure where you can, and keep printing in `cli.py` only.

## How to work (about two days)
1. Read this file and `tests/test_acceptance.py` fully before writing code.
2. Build `Task` first, then `storage`, then the CLI one command at a time. Run `pytest -x -q` constantly.
3. Write at least **ten** of your own unit tests in `tests/test_unit.py`: validation rules, the round trip, storage errors. Use `parametrize` and `tmp_path`.
4. Add type hints everywhere and run `mypy --strict src` until it is clean.
5. Run `ruff check . && ruff format .`.
6. Install it (`pip install -e ".[dev]"`) and use the real `tasks` command for a day.

## Done when (your rubric)
- [ ] All acceptance tests pass.
- [ ] At least ten meaningful unit tests of your own pass, and you can say what bug each one would catch.
- [ ] `mypy --strict src` and `ruff check .` report nothing.
- [ ] `pip install -e .` works and the `tasks` command runs.
- [ ] You can explain every file without looking, including why errors are turned into exit codes in one place.

## Stretch
- `edit ID --title ... --priority ...` and `list --due-before DATE`.
- Write to a temporary file and rename it, so a crash never leaves a half-written tasks file.
- A `--json` flag for `list`.
- Record the project in your own README with a short demo.
