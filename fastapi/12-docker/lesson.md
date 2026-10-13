# Module 12 (FastAPI): Docker and deployment

By the end you can package the Study API as a container image, run it with its configuration given from outside, check that it starts, keeps its data and stops cleanly, and deploy it to a host. The project is `fastapi/study-api`.

**Before you start:** finish the background work lesson (`../12-background/lesson.md`). You need Docker installed and running: Docker Desktop on Windows or macOS, or Docker Engine on Linux. Check with `docker --version`.

**What you write:** the Study API folder has a `Dockerfile` and a `.dockerignore` made of TODO comments. Fill them in (TODOs 28 and 29). The sections below explain each instruction. They do not give you the lines.

Run this module's tests with `pytest tests/test_deployment.py`. These 12 tests read the two files as text, so they run without Docker. All 12 should pass when you finish. A bare `pytest` runs all 117 tests: the 88 of weeks 10 to 12, and the 29 of the bonus module 13, which fail until you do that module.

**How to read the examples:** the examples use a made-up notes app, not the Study API. Section 7 is the one place that uses the real project, with commands you run yourself.

## 1. What a container is
An **image** is a packaged file system with the code, the Python packages and the start command, built once. A **container** is a running copy of an image. You can start many containers from one image, and stop and delete them, without changing the image.

The image is built from a **Dockerfile**, one instruction at a time. Each instruction makes a **layer**, and Docker caches the layers. A rebuild reuses every layer up to the first one that changed. Everything after that layer is built again. That is why the order of instructions matters, and section 2 comes back to it.

The image holds no configuration that differs between machines. The database address, the secret key and the port are given when the container starts, with environment variables. The same image then runs on your laptop and on a host, with different settings.

## 2. The Dockerfile, instruction by instruction
Each instruction answers one question:

- **`FROM`** picks the base image. Pin the version, such as `python:3.12-slim`. An image tag like `latest` changes under you, so the same Dockerfile can build a different image next month. The `slim` variant is small, but it has no compiler and no `curl`.
- **`ENV`** sets an environment variable in the image. Use it for defaults that are safe to publish. Anything that is a secret never goes here, because `docker history` shows every `ENV` line to anyone who has the image.
- **`WORKDIR`** sets the folder that later instructions run in.
- **`COPY`** copies files from your folder (the build context) into the image. Copy `requirements.txt` on its own first, then install, then copy the code. When only the code changes, the install layer is still cached, and the build takes seconds, not minutes.
- **`RUN`** runs a command during the build. `pip install --no-cache-dir` skips pip's download cache, so the cache does not end up in the image.

**`.dockerignore`** lists the files the build must not send at all. Without it, `COPY . .` would copy your virtual environment, your `.env` file with real secrets, a local `study.db`, and the git history. Each line is a pattern. A pattern such as `*.db` covers every database file. Lines that start with `#` are comments.

**Try it:** run `docker build` on the reference image in your own copy and note how long it takes. Change one line in `app/schemas.py`, build again, and read which steps are marked `CACHED` in the output. Then change `requirements.txt` and build again. Explain which steps ran again, and why.

## 3. A user that is not root, the port, and the start command
Processes in a container run as root unless the Dockerfile says otherwise. Create a user with a fixed user id, and switch to it with `USER` before the start command. If someone breaks into the app, that user has fewer rights than root.

**`EXPOSE`** documents the port the app listens on. It does not open the port. The port is opened when you run the container, with `-p`.

The app must listen on `0.0.0.0`, not the default `127.0.0.1`. An address of `127.0.0.1` means "only from inside this container", so nothing outside can reach the app. Uvicorn takes this as `--host`.

The port itself comes from the platform. Hosts such as Render set a `PORT` variable and expect the app to listen on it. Read `PORT` in the start command, and use 8000 when it is not set, so the image also works on a laptop.

**The start command.** Two forms exist:

```dockerfile
CMD python main.py          # shell form: Docker runs it through /bin/sh -c
CMD ["python", "main.py"]   # exec form: Docker runs the program directly
```

The shell form lets the shell expand `${PORT}`. The exec form is the one you want for the server itself, because `docker stop` sends SIGTERM to the first process in the container. If that process is a shell, the shell may not pass the signal on, and Docker waits ten seconds and then kills the container. A command with `sh -c` plus `exec` gets both: the shell reads `PORT`, then replaces itself with the server, so the server is the process that receives the signal.

The Study API also runs its migrations before the server starts. The `&&` operator runs the second command only if the first succeeds. If the migration fails, the server never starts, and the logs say why.

**Try it:** write a notes-app `CMD` in exec form that runs `python -m http.server $PORT`. Then try the same command in shell form, and explain why the exec form cannot read `$PORT`. Keep both answers, and decide which one the Study API needs.

## 4. Configuration: given at run time, never baked in
The Study API reads its settings from the environment (module 10 of this track). The image provides the defaults that are safe to publish. The rest comes at run time:

| Variable | Set where | Notes |
|---|---|---|
| `STUDY_SECRET_KEY` | At run time, from the platform's secret store | Required, at least 32 characters. Never in the image or in git |
| `STUDY_DATABASE_URL` | The image sets a default in `/data` | Change it only to point at a different database |
| `STUDY_ACCESS_TOKEN_MINUTES` | At run time, if you want a different lifetime | Defaults to 30 |
| `STUDY_MAX_WORDS` | At run time, if you want a different limit | Defaults to 500 |
| `PORT` | The platform sets it | Defaults to 8000 |

On your machine, keep the values in a file that `.dockerignore` excludes, and pass it with `--env-file`. Platforms have their own secret stores, and you enter the values in their dashboard.

Two warnings. Anyone who can run `docker inspect` on a container sees its environment variables. And a value passed with `-e` shows in your shell history. Use a secret store wherever one exists.

**Try it:** build the image, then run it without a secret key. Read the error the container prints, and find the line that names the missing setting.

## 5. Data that outlives the container
A container's file system disappears when the container is removed. A SQLite file written inside the container disappears with it. The Study API avoids this in two steps:

- The image makes `/data` a folder that the app user owns, and points the database address at a file inside it.
- You mount a **volume** at `/data` when you run the container. A named volume is kept by Docker after the container is removed, and the next container can mount it again.

Migrations run each time the container starts, so a new container with an old volume upgrades the database if it needs to, and does nothing if it does not.

This works for one container with one database file. Two containers writing one SQLite file, or a platform with no persistent disk, need a different database. PostgreSQL is the usual choice. Section 8 explains the change, and the module does not cover it.

**Try it:** run the container with a named volume, create a summary, remove the container, and start a new one with the same volume. Read the summary back. Then start a third container with no volume, and check whether the summary is there.

## 6. A health check
A container can be running and still broken. A health check tells Docker, and the platform, whether the app answers. Docker runs the check command every `--interval` and marks the container `starting`, `healthy` or `unhealthy`. The first failures after the start period do not count.

The check should call the same route the platform calls, `/health`, on the port the app actually listens on. The slim image has no `curl`, so use Python to make the request. Use the JSON-array form of the command. Inside a shell string, the nested quotes for the port would be hard to read.

**Try it:** start the container with `--health-cmd "exit 1"`, which replaces the check with one that always fails. Wait for two intervals, and read the status with `docker inspect --format "{{.State.Health.Status}}"`. It should say `unhealthy`. Then run the container with the real check, and read the status again. What would a platform do with an unhealthy container?

## 7. Build, run and check (on the Study API)
From `fastapi/study-api`:

```bash
docker build -t study-api .
docker volume create study-data
docker run -d --name study-api -e STUDY_SECRET_KEY="a-test-key-with-at-least-32-characters" -v study-data:/data -p 8000:8000 study-api
```

Wait about 15 seconds, then check each of these:

```bash
curl http://127.0.0.1:8000/health
docker inspect --format "{{.State.Health.Status}}" study-api
docker exec study-api id
docker stop study-api
docker inspect --format "{{.State.ExitCode}}" study-api
```

Expected results: `/health` returns `{"status":"ok"}`. The health status is `healthy`, once the first check has run. `id` shows a user id other than 0. The stop finishes in about a second, and the exit code is 0. Create a summary first, with a `POST` to `/summaries`. Then remove the container with `docker rm study-api`, run the same `docker run` command again, and read the summary back with `curl http://127.0.0.1:8000/summaries/1`. The summary should still be there, because the volume kept the database.

On Windows PowerShell, use `curl.exe` instead of `curl`, because `curl` there runs a different program. The `-e` and `-v` options are the same.

**Try it:** run the container with `-e PORT=9000` and `-p 8001:9000`. Check `/health` on port 8001, and read the health status after a minute. Which port does the health check use, and why?

## 8. Deploying to a host
The repo gives you the checklist, `deploy-checklist.md`. The steps are yours to do, because they need your account on the host. For a host such as Render, the settings are:

- A web service that builds from the Dockerfile, with the folder set to `fastapi/study-api` or the repo root, depending on the host.
- A health check path of `/health`.
- The secret key generated by the platform, never typed into a file.
- A persistent disk mounted at `/data` if the platform offers one, so the SQLite file survives a redeploy. Free plans often do not, and then the data is lost on each redeploy.

When the data needs to outlive one machine, switch to PostgreSQL. That needs a different async driver, a different address format, and a migration run against the new database. The Django track's deployment module covers the same problem with a different framework.

After the deploy, run the smoke tests in the checklist on the live URL, over HTTPS, using a test account.

## 9. Common mistakes
- A secret written into the image, with `ENV`, `ARG` or a copied `.env` file. `docker history` keeps it.
- No `.dockerignore`, so the virtual environment, the database file and the git history are copied into the image.
- Running as root, because the `USER` line is missing.
- Listening on `127.0.0.1` inside the container. The app then runs, but no request from outside reaches it.
- Shell-form `CMD` for the server, so `docker stop` takes ten seconds and the app gets no chance to shut down cleanly.
- Copying the code before the requirements, so every code change reinstalls every package.
- A `latest` base image, so the same Dockerfile builds a different image later.
- Data in the container's own file system, lost when the container is removed.
- Shipping the test packages in the image. This module installs one file of requirements, so pytest is in the image too. A real project keeps development packages in a separate file.

## 10. What this module does not cover
- A production server. Uvicorn runs alone here. The advanced tier of the syllabus covers Gunicorn with Uvicorn workers.
- PostgreSQL, and a database that several containers share.
- A pipeline that builds and deploys on every push (CI/CD).
- Secret rotation, and a store that is more than the platform's dashboard.
- Scaling to several instances, and zero-downtime deploys.
- The real model call, and rate limits. The summary and the flashcards still come from stand-in functions. The bonus module 13 adds both.

## Exit checklist
- [ ] I can say what goes into an image, what goes into a container, and what the environment provides at run time
- [ ] I can order the Dockerfile so that a code change does not reinstall the packages, and say what `.dockerignore` is for
- [ ] I can explain why the app runs as a non-root user, why it listens on `0.0.0.0`, and why the start command uses `exec`
- [ ] I can keep a secret out of the image, and say what `docker inspect` and `docker history` reveal
- [ ] I can keep data across container restarts with a named volume
- [ ] I can check the health status, and say which route and port it uses
- [ ] `pytest tests/test_deployment.py` passes all 12 tests, and `pytest --ignore=tests/test_ai.py` passes all 88
