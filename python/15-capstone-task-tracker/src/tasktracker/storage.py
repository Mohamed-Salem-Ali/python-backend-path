"""Reading and writing the tasks file (JSON)."""

from pathlib import Path

from .models import Task


def load(path: Path) -> tuple[int, list[Task]]:
    """Return (next_id, tasks). A missing file means no tasks yet: (1, []).
    A file that is not valid JSON or has the wrong shape raises StorageError."""
    # TODO
    ...


def save(path: Path, next_id: int, tasks: list[Task]) -> None:
    """Write {"next_id": ..., "tasks": [...]} to the file as JSON (UTF-8)."""
    # TODO
    ...
