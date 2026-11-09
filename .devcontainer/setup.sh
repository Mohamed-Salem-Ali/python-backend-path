#!/usr/bin/env bash
# Runs once, when the dev container is created. Safe to run again.
set -euo pipefail

pip install --quiet -r requirements-dev.txt

for project in django/gameya_site fastapi/study-api; do
  echo "Installing $project/requirements.txt into $project/.venv"
  python -m venv "$project/.venv"
  "$project/.venv/bin/pip" install --quiet -r "$project/requirements.txt"
done

echo
echo "Ready. Start with python/WEEK-1.md, and check your progress any time with:"
echo "  python scripts/progress.py"
echo "In the Django or FastAPI folder, activate its environment first: source .venv/bin/activate"
