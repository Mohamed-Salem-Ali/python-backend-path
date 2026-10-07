"""Module 14 check. Finish the package in gameya_toolkit/, then run:

    python python/14-packaging/exercises.py

It reads pyproject.toml, imports the package from src/, and exercises the command-line entry point.
"""

import contextlib
import io
import re
import sys
import tomllib
from importlib import import_module
from pathlib import Path

PACKAGE_DIR = Path(__file__).parent / "gameya_toolkit"


def fail(message: str) -> None:
    raise AssertionError(message)


def check_metadata() -> dict:
    with open(PACKAGE_DIR / "pyproject.toml", "rb") as f:
        config = tomllib.load(f)

    build = config.get("build-system", {})
    assert build.get("build-backend") == "setuptools.build_meta", "keep the [build-system] table"

    project = config.get("project", {})
    if not project:
        fail("pyproject.toml: the [project] table is empty. Fill in the metadata.")
    assert project.get("name") == "gameya-toolkit", "project.name must be 'gameya-toolkit'"
    version = project.get("version", "")
    assert re.fullmatch(r"\d+\.\d+\.\d+", version), (
        f"project.version must look like 0.1.0, got {version!r}"
    )
    assert project.get("description", "").strip(), "project.description is missing"
    assert project.get("readme") == "README.md", "project.readme must be 'README.md'"
    assert str(project.get("requires-python", "")).startswith(">=3."), (
        "project.requires-python must be like '>=3.12'"
    )
    assert isinstance(project.get("dependencies"), list), (
        "project.dependencies must be a list (it can be empty)"
    )
    license_value = project.get("license")
    assert license_value, 'project.license is missing (for example {text = "MIT"})'
    scripts = project.get("scripts", {})
    assert scripts.get("gameya-toolkit") == "gameya_toolkit.cli:main", (
        'add [project.scripts] with: gameya-toolkit = "gameya_toolkit.cli:main"'
    )
    return project


def check_code(project: dict) -> None:
    sys.path.insert(0, str(PACKAGE_DIR / "src"))
    try:
        package = import_module("gameya_toolkit")
    except ImportError as e:
        fail(f"could not import gameya_toolkit: {e}")
    version = getattr(package, "__version__", None)
    assert version, "define __version__ in src/gameya_toolkit/__init__.py"
    assert version == project["version"], (
        f"__version__ {version!r} must match pyproject version {project['version']!r}"
    )
    assert package.format_money(125050) == "1,250.50 EGP"

    cli = import_module("gameya_toolkit.cli")

    def run(argv: list[str]) -> tuple[int, str]:
        out = io.StringIO()
        code = 0
        with contextlib.redirect_stdout(out):
            try:
                result = cli.main(argv)
                code = 0 if result is None else result
            except SystemExit as e:  # argparse exits for --version
                code = e.code if isinstance(e.code, int) else 0
        return code, out.getvalue().strip()

    code, text = run(["--version"])
    assert code == 0 and text == f"gameya-toolkit {version}", f"--version printed {text!r}"
    code, text = run(["format", "125050"])
    assert code == 0 and text == "1,250.50 EGP", f"format printed {text!r}"
    code, text = run(["format", "5", "--currency", "USD"])
    assert code == 0 and text == "0.05 USD", f"format --currency printed {text!r}"


if __name__ == "__main__":
    metadata = check_metadata()
    check_code(metadata)
    print("All checks passed")
    print("Now install it for real:  pip install -e python/14-packaging/gameya_toolkit")
    print("Then run:                  gameya-toolkit format 125050")
