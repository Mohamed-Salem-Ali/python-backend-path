# Module 14: Packaging and dependency management

By the end you can turn a folder of code into an installable package with a command-line tool, manage its dependencies, and build it for distribution.

## 1. Why package
A script works on your machine. A **package** works anywhere: it declares what it needs, installs with one command, can be imported from any folder, and can expose commands. Every library you `pip install` is a package, and so will your Django and FastAPI projects be.

## 2. Vocabulary
- **Module:** one `.py` file. **Package:** a folder of modules (with `__init__.py`), Module 06.
- **Distribution:** what you publish: a **wheel** (`.whl`, ready to install) and/or an **sdist** (`.tar.gz`, source).
- **Build backend:** the tool that turns the project into a distribution (`setuptools`, `hatchling`, `flit`, `poetry-core`).
- **PyPI:** the public index `pip` downloads from. **TestPyPI** is a sandbox for practising.

## 3. `pyproject.toml`: the one config file
It replaces the old `setup.py` and `setup.cfg`. TOML is a simple `key = value` format with `[tables]`.

```toml
[build-system]                       # how to build the project
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]                            # what the project is
name = "gameya-toolkit"
version = "0.1.0"
description = "Format Gameya money amounts"
readme = "README.md"
requires-python = ">=3.12"
license = {text = "MIT"}
dependencies = [
  "requests>=2.31",
]

[project.optional-dependencies]      # extras: pip install "gameya-toolkit[dev]"
dev = ["pytest>=8", "ruff"]

[project.scripts]                    # console commands
gameya-toolkit = "gameya_toolkit.cli:main"

[tool.setuptools.packages.find]      # where the code lives
where = ["src"]
```
Tools such as Ruff, pytest and mypy also read their settings from `[tool.*]` tables in this file (this repo's `pyproject.toml` does).

## 4. The `src` layout
```text
gameya_toolkit/
├── pyproject.toml
├── README.md
├── src/
│   └── gameya_toolkit/
│       ├── __init__.py
│       ├── money.py
│       └── cli.py
└── tests/
    └── test_money.py
```
Putting code under `src/` stops you accidentally importing the folder instead of the installed package, so tests exercise what users will actually get.

## 5. Install it for development: editable mode
```bash
cd gameya_toolkit
python -m venv .venv && .venv\Scripts\Activate.ps1    # always use a venv
pip install -e .                  # editable: changes to the code take effect immediately
pip install -e ".[dev]"           # also install the dev extras
gameya-toolkit --version          # your console script now exists
python -c "import gameya_toolkit; print(gameya_toolkit.__version__)"
```
`pip show gameya-toolkit` and `pip list` confirm what got installed.

## 6. Console scripts and `__main__`
The `[project.scripts]` entry `gameya-toolkit = "gameya_toolkit.cli:main"` creates an executable that imports `gameya_toolkit.cli` and calls `main()`. Its return value becomes the exit code (`sys.exit(main())`). You can also add `src/gameya_toolkit/__main__.py` so `python -m gameya_toolkit` works.

## 7. Versions and dependencies
- **Semantic versioning:** `MAJOR.MINOR.PATCH`. Breaking change: bump MAJOR. New feature: MINOR. Bug fix: PATCH.
- Keep the version in **one** place if you can. In this exercise it lives in `pyproject.toml` and `__version__`; real projects often read it from one (`dynamic = ["version"]`) or from git tags.
- **Specifiers:** `requests>=2.31` (at least), `requests~=2.31` (compatible: `>=2.31, <3`), `requests==2.31.0` (exact). Libraries declare **ranges**; applications **pin** exact versions.
- `requirements.txt` (from `pip freeze`) is the exact set for one environment. `pyproject.toml` says what the project needs in general. Use both: libraries lean on `pyproject.toml`, deployed apps on a pinned lock.
- Separate runtime dependencies from dev ones (tests, linters) with optional dependencies or dependency groups.

## 8. Build and publish
```bash
pip install build
python -m build                   # creates dist/gameya_toolkit-0.1.0-py3-none-any.whl and .tar.gz
pip install dist/gameya_toolkit-0.1.0-py3-none-any.whl     # install what users would get
```
Publishing uses `twine upload` (TestPyPI first) with an API token. **Never commit tokens** or `dist/` to Git. A wheel is just a zip: `python -m zipfile -l dist/*.whl` shows what ships.

## 9. Modern tools
`pip` + `venv` is the foundation and enough for now. You will meet:
- **uv:** a very fast installer, resolver and project manager (`uv init`, `uv add requests`, `uv run pytest`, `uv.lock`).
- **Poetry / PDM / Hatch:** project managers with lock files.
- **pipx:** installs command-line tools (like `ruff`, `httpie`) in their own isolated environments.
They all read and write the same standard `pyproject.toml`, so what you learn here carries over.

## 10. Habits
- One virtual environment per project; never `sudo pip install`.
- Commit `pyproject.toml` (and a lock file for apps); never commit `.venv`, `dist/`, `*.egg-info/` or tokens.
- Pin application dependencies; give libraries sensible ranges.
- Keep the README honest and the version bumped when you release.

## Check your understanding
1. What is the difference between a module, a package and a distribution?
2. What goes in `[build-system]` and what goes in `[project]`?
3. Why use the `src` layout?
4. What does `pip install -e .` do differently from `pip install .`?
5. How does `[project.scripts]` turn a Python function into a shell command?
6. When do you pin a dependency, and when do you give a range?
7. Why do you never commit `.venv`, `dist/` or an upload token?

## Do the exercises
The package skeleton is in `gameya_toolkit/`.
1. Fill in `pyproject.toml` (metadata and the console script), `__version__` in `__init__.py`, and `main()` in `cli.py`.
2. Run `python python/14-packaging/exercises.py`. It tells you what is missing.
3. Then install it for real: `pip install -e python/14-packaging/gameya_toolkit` and run `gameya-toolkit format 125050`.
4. Stretch: `pip install build`, run `python -m build` inside `gameya_toolkit/`, and list the wheel's contents with `python -m zipfile -l dist/*.whl`. Delete `dist/` afterwards (it is git-ignored).
