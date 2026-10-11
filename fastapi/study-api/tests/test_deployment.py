"""Module 12 (Docker) acceptance tests: the image file, and what it leaves out. Do not edit.

Run from fastapi/study-api:  pytest tests/test_deployment.py

These tests read the Dockerfile and .dockerignore as text, so they run without Docker. The lesson,
section 7, has the commands that build the image and run it. The tests need the Dockerfile (TODO 28)
and the .dockerignore file (TODO 29).
"""

import re
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]


def read_lines(name):
    # Comment lines are ignored, so a TODO that mentions an instruction cannot pass for it.
    lines = (PROJECT / name).read_text(encoding="utf-8").splitlines()
    return [line.strip() for line in lines if line.strip() and not line.lstrip().startswith("#")]


def dockerfile():
    return "\n".join(read_lines("Dockerfile"))


def instructions():
    # A line that ends in a backslash continues on the next line, so join them into one instruction.
    joined, current = [], ""
    for line in read_lines("Dockerfile"):
        if line.endswith("\\"):
            current += line[:-1] + " "
        else:
            joined.append(current + line)
            current = ""
    return joined


def start_command():
    # The CMD instruction itself. A CMD inside a HEALTHCHECK instruction does not count.
    return next((line for line in instructions() if line.startswith("CMD")), "")


def test_the_image_starts_from_a_pinned_python_312():
    assert re.search(r"^FROM python:3\.12\S*\s*$", dockerfile(), re.M)


def test_the_app_runs_as_a_user_that_is_not_root():
    users = re.findall(r"^USER\s+(\S+)", dockerfile(), re.M)
    assert users and users[-1] not in ("root", "0")


def test_no_secret_is_written_into_the_image():
    assert "STUDY_SECRET_KEY" not in dockerfile()


def test_the_requirements_are_copied_before_the_code():
    text = dockerfile()
    requirements = text.find("COPY requirements.txt")
    code = text.find("COPY app")
    assert 0 <= requirements < code


def test_the_packages_install_without_a_download_cache():
    assert re.search(r"pip install[^\n]*--no-cache-dir[^\n]*-r requirements\.txt", dockerfile())


def test_the_database_file_is_in_the_data_folder():
    assert re.search(r"STUDY_DATABASE_URL=\S*/data/", dockerfile())


def test_the_container_listens_on_all_interfaces_and_the_platform_port():
    command = start_command()
    assert "--host 0.0.0.0" in command
    assert "PORT" in command


def test_the_start_command_migrates_before_it_serves():
    command = start_command()
    assert 0 <= command.find("alembic upgrade head") < command.find("uvicorn")


def test_uvicorn_replaces_the_shell_so_stop_reaches_it():
    assert "exec uvicorn" in start_command()


def test_the_port_is_documented_with_expose():
    assert re.search(r"^EXPOSE\s+8000\b", dockerfile(), re.M)


def test_a_health_check_probes_the_health_route():
    text = dockerfile()
    assert re.search(r"^HEALTHCHECK\b", text, re.M)
    assert "/health" in text


def test_the_dockerignore_keeps_secrets_and_local_files_out():
    entries = set(read_lines(".dockerignore"))
    assert {".env", "*.db", ".venv", "__pycache__", "tests"} <= entries
