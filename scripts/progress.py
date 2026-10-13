"""Show what passes so far, across the three tracks, in one table.

Run it from the repo root:

    python scripts/progress.py            # all three tracks
    python scripts/progress.py python     # one track: python, django or fastapi

It only reads and runs your code; it changes nothing. Each Python module counts as passing when its
check exits cleanly (`exercises.py`, or `check_tests.py` for module 13, or the capstone's tests).
The Django and FastAPI projects are run with pytest, and each test file shows how many of its tests
pass. Those two need their own requirements installed: the script uses the project's `.venv` if
there is one, and the Python that runs this script otherwise.
"""

from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PYTHON = ROOT / "python"
DJANGO = ROOT / "django" / "gameya_site"
FASTAPI = ROOT / "fastapi" / "study-api"
TIMEOUT = 300

DJANGO_FILES = {
    "test_architecture": "01 Architecture",
    "test_models": "02 Models",
    "test_queries": "02 Queries",
    "test_admin_forms": "03 Admin and forms",
    "test_class_views": "04 Views",
    "test_templates": "05 Templates",
    "test_api": "06 DRF",
    "test_middleware_signals": "07 Middleware and signals",
    "test_pytest_suite": "08 Testing",
    "test_performance": "09 Caching and performance",
    "test_tasks": "10 Background tasks",
    "test_security": "11 Auth and security",
    "test_deployment": "12 Deployment",
}

FASTAPI_FILES = {
    "test_basics": "Basics",
    "test_validation": "Pydantic",
    "test_database": "The database",
    "test_auth": "Auth",
    "test_background": "Background work",
    "test_deployment": "Docker",
}


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str] | None:
    """Run a command and capture its output. Return None if it does not finish in time."""
    try:
        return subprocess.run(
            command, cwd=cwd, capture_output=True, text=True, timeout=TIMEOUT, env=os.environ
        )
    except subprocess.TimeoutExpired:
        return None


def line(label: str, result: str) -> None:
    print(f"  {label:<56} {result}")


def python_track() -> tuple[int, int]:
    print("\nPython (python/)")
    done = total = 0
    for folder in sorted(p for p in PYTHON.iterdir() if p.is_dir() and p.name[:2].isdigit()):
        if (folder / "check_tests.py").exists():
            command = [sys.executable, str(folder / "check_tests.py")]
            cwd = ROOT
        elif (folder / "exercises.py").exists():
            command = [sys.executable, str(folder / "exercises.py")]
            cwd = ROOT
        elif (folder / "tests").is_dir():
            command = [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"]
            cwd = folder
        else:
            continue
        total += 1
        result = run(command, cwd)
        if result is None:
            line(folder.name, "timed out")
        elif result.returncode == 0:
            done += 1
            line(folder.name, "PASS")
        else:
            line(folder.name, "not yet")
    return done, total


def project_python(project: Path, probe: str) -> str | None:
    """The Python to use for a project: its .venv if present, else this one, if it has the deps."""
    candidates = [
        project / ".venv" / "Scripts" / "python.exe",
        project / ".venv" / "bin" / "python",
    ]
    for interpreter in [*map(str, filter(Path.exists, candidates)), sys.executable]:
        check = run([interpreter, "-c", f"import {probe}"], project)
        if check is not None and check.returncode == 0:
            return interpreter
    return None


def pytest_by_file(interpreter: str, project: Path, extra: list[str]) -> dict[str, Counter] | None:
    """Run pytest once, and count the passed and total tests per test file."""
    with tempfile.TemporaryDirectory() as tmp:
        report = Path(tmp) / "report.xml"
        command = [interpreter, "-m", "pytest", "-q", "-p", "no:cacheprovider", *extra]
        result = run([*command, f"--junitxml={report}"], project)
        if result is None or not report.exists():
            return None
        counts: dict[str, Counter] = {}
        for case in ET.parse(report).iter("testcase"):
            parts = case.get("classname", "").split(".")
            name = next((part for part in parts if part.startswith("test_")), "")
            if not name:
                continue
            tally = counts.setdefault(name, Counter())
            tally["total"] += 1
            if not any(child.tag in ("failure", "error", "skipped") for child in case):
                tally["passed"] += 1
        return counts


def project_track(title: str, project: Path, probe: str, files: dict, extra: list[str]):
    print(f"\n{title}")
    interpreter = project_python(project, probe)
    if interpreter is None:
        requirements = (project / "requirements.txt").relative_to(ROOT).as_posix()
        line("skipped", f"install {requirements} first")
        return 0, len(files)
    counts = pytest_by_file(interpreter, project, extra)
    if counts is None:
        line("pytest did not finish", "run pytest in the project folder to see why")
        return 0, len(files)
    done = 0
    for name, label in files.items():
        tally = counts.get(name)
        if not tally:
            line(f"{label} ({name}.py)", "not collected (an import or setup error)")
            continue
        passed, total = tally["passed"], tally["total"]
        done += passed == total
        status = "PASS" if passed == total else "not yet"
        line(f"{label} ({name}.py)", f"{passed:>3} of {total:<3} {status}")
    return done, len(files)


def main(argv: list[str]) -> int:
    tracks = argv or ["python", "django", "fastapi"]
    unknown = set(tracks) - {"python", "django", "fastapi"}
    if unknown:
        print(f"Unknown track: {', '.join(sorted(unknown))}. Use python, django or fastapi.")
        return 2
    summary = []
    if "python" in tracks:
        summary.append(("Python modules", *python_track()))
    if "django" in tracks:
        # --ds lets the run work before module 08 adds DJANGO_SETTINGS_MODULE to pytest.ini.
        found = project_track(
            "Django (django/gameya_site)",
            DJANGO,
            "django, pytest_django",
            DJANGO_FILES,
            ["--ds=config.settings", "circles/tests"],
        )
        summary.append(("Django test files", *found))
    if "fastapi" in tracks:
        found = project_track(
            "FastAPI (fastapi/study-api)", FASTAPI, "fastapi, pytest", FASTAPI_FILES, ["tests"]
        )
        summary.append(("FastAPI test files", *found))
    print()
    for label, done, total in summary:
        print(f"{label}: {done} of {total} pass")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
