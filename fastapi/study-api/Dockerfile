# The Study API image. Module 12 (Docker): fill in the TODO, then run the tests.
# Read the Docker lesson, sections 2 to 6, first. The tests skip lines that start with #.
#
# TODO 28: FROM the Python 3.12 slim image. Pin the version, not "latest" (section 2).
# TODO 28: ENV: set PYTHONDONTWRITEBYTECODE and PYTHONUNBUFFERED to 1 (section 2). Set
#          STUDY_DATABASE_URL to a SQLite file in /data (section 5). Never set
#          STUDY_SECRET_KEY here: it is given when the container runs (section 4).
# TODO 28: WORKDIR /app (section 2).
# TODO 28: COPY requirements.txt first, then RUN pip install with no download cache. The code
#          is copied after the install, so the install layer is reused (section 2).
# TODO 28: COPY alembic.ini, the app folder and the migrations folder (section 2).
# TODO 28: create a user with a fixed user id, and the /data folder owned by that user. Then
#          USER that user, so the app does not run as root (section 3).
# TODO 28: EXPOSE 8000, to document the port (section 3).
# TODO 28: HEALTHCHECK that calls /health on the port in PORT, with 8000 as the default
#          (section 6). Use the JSON-array form, so no shell quoting is needed.
# TODO 28: CMD: run the migrations, then replace the shell with uvicorn (exec), listening on
#          0.0.0.0 and on the port in PORT, with 8000 as the default. Section 3 explains why the
#          shell form is needed here, and why exec matters.
