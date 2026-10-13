# Contributing

Thanks for helping. This is a learning repo, so clarity matters more than cleverness.

- **Typos and unclear explanations:** open a pull request directly.
- **A check (`assert`) that is wrong or too strict:** open an issue with the input, the expected value and what you got.
- **New exercises or modules:** open an issue first so we agree on scope.

## Conventions
- Lessons are Markdown (`lesson.md`); exercises are `exercises.py` with `TODO` stubs and a `__main__` block of asserts that prints `All checks passed`.
- Do not commit solutions to exercises. Keep reference solutions out of this repo.
- Python 3.12, formatted and linted with [Ruff](https://docs.astral.sh/ruff/): `ruff format .` and `ruff check .`.
- Keep line length at 100.
- Before a pull request, run `python scripts/check_links.py`, so every relative link and heading link still resolves. CI runs it too, along with Ruff and a check that both projects' tests still load.
