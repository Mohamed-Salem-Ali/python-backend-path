"""Checks the quality of YOUR tests.

1. Your tests must pass against the real payments.py.
2. Then the checker plants one bug at a time in a copy of payments.py and runs your tests again.
   Every planted bug must make at least one of your tests fail ("caught").

Run:  python python/13-testing/check_tests.py
"""

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent

# (description, text to find in payments.py, text to replace it with)
MUTANTS = [
    ("parse_amount ignores thousands separators", '.replace(",", "")', ""),
    (
        "total() forgets the last entry",
        "return sum(c for _, c in self._entries)",
        "return sum(c for _, c in self._entries[:-1])",
    ),
    ("add() accepts zero", "if cents <= 0:", "if cents < 0:"),
    (
        "balance_of() counts everyone",
        "for m, c in self._entries if m == member",
        "for m, c in self._entries",
    ),
    (
        "convert() truncates instead of rounding",
        "return round(cents * rate)",
        "return int(cents * rate)",
    ),
    (
        "convert() asks for the rate twice",
        "rate = fetch_rate(currency)",
        "fetch_rate(currency)\n    rate = fetch_rate(currency)",
    ),
    (
        "load_ledger() hides a missing file",
        'data = json.loads(path.read_text(encoding="utf-8"))',
        'data = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {"entries": []}',
    ),
    ("today_label() uses the wrong format", '"%A %d %B %Y"', '"%d/%m/%Y"'),
]


def run_tests(directory: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-x", "--no-header", "-p", "no:cacheprovider", "."],
        cwd=directory,
        capture_output=True,
        text=True,
    )


def workspace(source_text: str) -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="check_tests_"))
    (tmp / "payments.py").write_text(source_text, encoding="utf-8")
    shutil.copy(HERE / "test_payments.py", tmp / "test_payments.py")
    return tmp


def main() -> int:
    source = (HERE / "payments.py").read_text(encoding="utf-8")
    test_source = (HERE / "test_payments.py").read_text(encoding="utf-8")

    todo = test_source.count("raise NotImplementedError")
    if todo:
        print(f"Not yet: {todo} place(s) in test_payments.py still say NotImplementedError.")
        print("Write those tests first, then run this checker again.")
        return 1

    tmp = workspace(source)
    result = run_tests(tmp)
    shutil.rmtree(tmp, ignore_errors=True)
    if result.returncode != 0:
        print("Your tests fail against the REAL payments.py. Fix them first:\n")
        print(result.stdout[-2000:] or result.stderr[-2000:])
        return 1
    print("Step 1 ok: your tests pass against the real code.\n")

    survivors = []
    for description, old, new in MUTANTS:
        assert old in source, f"checker bug: {old!r} not found in payments.py"
        tmp = workspace(source.replace(old, new, 1))
        caught = run_tests(tmp).returncode != 0
        shutil.rmtree(tmp, ignore_errors=True)
        print(f"  {'caught  ' if caught else 'SURVIVED'}  {description}")
        if not caught:
            survivors.append(description)

    print()
    if survivors:
        print(f"{len(survivors)} bug(s) got past your tests.")
        print("Add or sharpen a test for each SURVIVED line.")
        return 1
    print("All checks passed: your tests caught every planted bug.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
