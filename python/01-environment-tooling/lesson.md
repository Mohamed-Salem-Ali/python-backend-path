# Module 01: Environment & tooling

By the end you can run Python three ways, isolate a project's packages in a virtual environment, and read a basic error message.

## 1. What Python is, in one paragraph
Python is an **interpreter**: you give it text (source code) and it executes it line by line. `python` on your machine is a program that reads your `.py` file and runs it. You have Python 3.12 installed at `C:\Python312`. Check:

```powershell
python --version
py -0          # lists every Python version installed (Windows launcher)
```

## 2. Three ways to run code
1. **The REPL** (Read-Eval-Print Loop): type `python`, then code. Best for trying ideas.
   ```
   >>> 2 + 3
   5
   >>> "ab" * 3
   'ababab'
   >>> exit()
   ```
2. **A script**: put code in `hello.py`, then `python hello.py`. Best for anything you want to keep.
3. **A module**: `python -m something` runs an installed module, for example `python -m venv .venv`.

Try it: in the REPL, evaluate `10 / 3`, `10 // 3`, `10 % 3`, `2 ** 10`. Predict first.

## 3. Your first script
Create `hello.py`:

```python
name = input("What is your name? ")
print("Hello,", name)
print(f"Your name has {len(name)} letters")
```

Run it: `python hello.py`. Notes:
- `input()` always returns a **string**, even if you type digits.
- `f"...{expr}..."` is an f-string: it evaluates `expr` inside the braces.
- Indentation is part of the syntax in Python (we'll use it from the next module).

## 4. Why virtual environments exist
`pip install requests` normally installs into your global Python. Two projects might need different versions of the same package, and they would break each other. A **virtual environment (venv)** is a private folder with its own Python and its own packages for one project.

```powershell
cd D:\work\Career\Learning\practice\python
python -m venv .venv                 # create (once per project)
.venv\Scripts\Activate.ps1           # activate (every new terminal)
python -c "import sys; print(sys.prefix)"   # should point inside .venv
pip install requests
pip list
pip freeze > requirements.txt        # record exactly what is installed
deactivate                           # leave the venv
```

If PowerShell refuses to run the Activate script, run once:
`Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

Rules:
- **Never commit** `.venv` (add it to `.gitignore`). Commit `requirements.txt` instead; anyone can recreate the venv with `pip install -r requirements.txt`.
- One venv per project. The terminal prompt shows `(.venv)` when active.

## 5. pip in 5 commands
```powershell
pip install package
pip install package==1.2.3
pip uninstall package
pip list
pip show package      # where it is installed, its version, what it needs
```

## 6. Reading an error (Traceback)
Create `broken.py`:

```python
def divide(a, b):
    return a / b


print(divide(10, 0))
```

Run it. Read the traceback **from the bottom**:
1. The last line is the error type and message: `ZeroDivisionError: division by zero`.
2. The lines above show where it happened, innermost call last.

Common errors you will meet this week: `NameError` (a name that is not defined), `TypeError` (wrong type, such as `"a" + 1`), `SyntaxError` (code is not valid Python), `IndentationError`, `ValueError` (right type, bad value, such as `int("abc")`).

## 7. Editor setup (VS Code)
- Install the **Python** extension (ms-python.python) and **Ruff** for formatting/linting.
- `Ctrl+Shift+P` → "Python: Select Interpreter" → pick the one inside `.venv`.
- Use the integrated terminal (`` Ctrl+` ``).

## 8. Style basics (PEP 8)
- 4 spaces per indent level, `snake_case` for variables and functions, `UPPER_CASE` for constants, `CapWords` for classes.
- Docstrings for functions: `"""Say what it does."""`.
- Run `python -m this` once to read the Zen of Python.

## Check your understanding (answer aloud, then in notes.md)
1. What is the difference between running a script and using the REPL?
2. Why use a venv instead of installing globally?
3. How do you know the venv is active?
4. Why not commit `.venv`? What do you commit instead?
5. In a traceback, which line do you read first?

Then do `exercises.py`.

## Revision companion (optional)
An interactive summary of this lesson, generated with Google NotebookLM: [Mastering Python Foundations](https://notebooklm.link.google/0LMX09CyQQoX). Use it for a quick recap after you finish the lesson and the exercises. This lesson stays the source of truth; the link is hosted by Google and may change.
