"""Command-line entry point: the `gameya-toolkit` command."""

from . import __version__  # noqa: F401  (you will use it for --version)
from .money import format_money  # noqa: F401  (you will use it for the format command)


def main(argv: list[str] | None = None) -> int:
    """Build an argparse parser and run it. Return the exit code.

    Required behaviour:
      gameya-toolkit --version         prints "gameya-toolkit 0.1.0" (the real version), exit 0
      gameya-toolkit format 125050     prints "1,250.50 EGP"
      gameya-toolkit format 125050 --currency USD     prints "1,250.50 USD"
    """
    # TODO
    ...
    return 0
