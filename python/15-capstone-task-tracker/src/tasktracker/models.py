"""The data model. Design this first: it is the heart of the program."""

from dataclasses import dataclass

PRIORITIES = ("high", "normal", "low")  # highest first
MAX_TITLE = 80


class TaskError(Exception):
    """Base class for errors the program expects (bad input, missing task, bad file)."""


class ValidationError(TaskError):
    """The user gave invalid input (exit code 2)."""


class NotFound(TaskError):
    """There is no task with that id (exit code 1)."""


class StorageError(TaskError):
    """The tasks file cannot be read (exit code 1)."""


@dataclass
class Task:
    # TODO: id (int), title (str), done (bool, default False), priority (str, default "normal"),
    #       due (ISO date string or None), created (ISO date string)
    ...

    # TODO: validate in __post_init__: title must be 1-80 characters after stripping,
    #       priority must be one of PRIORITIES, due (if given) must be a real ISO date.
    #       Raise ValidationError with a clear message.

    # TODO: to_dict() and a from_dict() classmethod for saving and loading.
