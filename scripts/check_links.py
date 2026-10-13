"""Check that every relative link in the repo's Markdown files points at a file that exists.

Run it from the repo root:

    python scripts/check_links.py

Links to a heading (`file.md#some-heading`) are checked too, using GitHub's rules for turning a
heading into an anchor. Web links (http, https, mailto) are not fetched. Code blocks are skipped.
It prints each broken link and exits with 1 if there is any, so CI can run it.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {".venv", "venv", "node_modules", ".git", ".pytest_cache"}
FENCE = re.compile(r"^(```|~~~).*?^\1", re.S | re.M)
LINK = re.compile(r"\]\(([^)\s]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.*)$", re.M)


def slug(heading: str) -> str:
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading.strip().lower())
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def anchors(path: Path) -> set[str]:
    found: set[str] = set()
    seen: dict[str, int] = {}
    for heading in HEADING.findall(FENCE.sub("", path.read_text(encoding="utf-8"))):
        base = slug(heading)
        count = seen.get(base, 0)
        seen[base] = count + 1
        found.add(base if count == 0 else f"{base}-{count}")
    return found


def markdown_files() -> list[Path]:
    return sorted(
        path
        for path in ROOT.rglob("*.md")
        if not SKIP_DIRS & set(path.relative_to(ROOT).parts) and path.name != "tasks.md"
    )


def main() -> int:
    broken = 0
    for page in markdown_files():
        text = FENCE.sub("", page.read_text(encoding="utf-8"))
        for target in LINK.findall(text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            path_part, _, fragment = target.partition("#")
            destination = (page.parent / path_part).resolve() if path_part else page
            where = page.relative_to(ROOT).as_posix()
            if not destination.exists():
                print(f"{where}: missing file: {target}")
                broken += 1
            elif fragment and destination.suffix == ".md" and fragment not in anchors(destination):
                print(f"{where}: missing heading: {target}")
                broken += 1
    print(f"{broken} broken link(s)" if broken else "All links resolve")
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
