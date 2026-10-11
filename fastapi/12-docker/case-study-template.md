# Case study: Study API (template)

Copy this file into your own portfolio repo, and fill in each heading. The word limits are guides for about 600 words in all. Replace every line in italics with your own text. Delete the italic guidance when you are done.

**Live:** _(URL from the deploy checklist)_ **Repository:** _(URL)_ **Commit shipped:** _(hash)_

## 1. The problem (about 80 words)
_Who would use a study summary service, and what did they do before? Name one concrete situation, such as reading a long chapter the night before a test and remembering only the first page._

## 2. What it does (about 100 words)
_List the main things a user can do, in short sentences. Say what a visitor can do without signing in (create a summary, read the docs), and what a signed-in user can do (see their own summaries, read their own profile)._

## 3. How it is built (about 120 words)
_Describe the parts in order: the routes, the request and response models, the database and its migrations, the sign-in with tokens, the background job that makes flashcards, and the container. Name the tools (FastAPI, Pydantic, SQLAlchemy, Alembic, PyJWT, pwdlib, uvicorn, Docker). One sentence per part._

## 4. Decisions and trade-offs (about 120 words)
_Pick two decisions. For each: what you chose, what you did not choose, and what it costs. Example: a background job that runs in the web process, which is simple, but loses its work if the process restarts._

## 5. Security (about 80 words)
_Summarise how sign-in works (hashed passwords, signed tokens with a short lifetime, one 401 for every failure). Name one open risk, such as deletes that any caller can make, and say what you would do about it. Do not describe a weakness in a way that helps an attacker, and do not include any secret._

## 6. Measured results (about 60 words)
_Give the numbers you measured for the frozen commit, and how you measured each one. Examples: the image size from `docker image ls`, the time `docker stop` took, the number of tests and how many pass. Say which command produced each number._

## 7. What I would change next (about 40 words)
_One or two things, and why. Be specific: PostgreSQL for more than one instance, a status route for background jobs, or retries for the model call._

---

**Checklist before you publish:** the live link opens over HTTPS; the repo README passes a clean-clone test (`docker build` and `pytest` both work from a fresh clone); every number matches the frozen commit; no secret, password, or personal data appears in the text.
