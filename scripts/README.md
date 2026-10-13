# Scripts

Small helpers for learners and contributors. Run them from the repo root. They use only the standard library, so they work in any Python 3.12 environment.

| File | What it does | Run it when |
|---|---|---|
| [progress.py](progress.py) | Runs every Python module's check and both projects' tests, and prints one line per module or test file, with how many tests pass | Whenever you want to see where you are, for example on Day 6 |
| [check_links.py](check_links.py) | Checks that every relative link and heading link in the Markdown files resolves | Before you open a pull request; CI runs it on every push |

`progress.py` takes an optional track name: `python scripts/progress.py django`. For the Django and FastAPI parts it needs that project's requirements. It uses the project's own `.venv` folder if you made one there (as the week 5 and week 10 setup steps do), and the Python that runs the script otherwise. If neither has the requirements, it says so and skips that project.

Both scripts only read your files and run your checks; they never change anything.
