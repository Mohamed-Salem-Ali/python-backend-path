"""The command line. Keep it thin: parse arguments, call the model and storage, print."""

from .models import NotFound, StorageError, ValidationError  # noqa: F401  (you will use these)


def main(argv: list[str] | None = None) -> int:
    """Run the program and return the exit code (0 ok, 1 not found or file problem, 2 bad input).

    Global options:  --file PATH (default tasks.json)   --today YYYY-MM-DD (default: today)
    Commands: add, list, done, remove, stats. See README.md for the exact output formats.
    """
    # TODO
    ...
    return 0
