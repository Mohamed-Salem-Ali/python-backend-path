"""The Study API application. Module 10 (FastAPI basics): fill in the TODOs.

Start the server from fastapi/study-api:  uvicorn app.main:app --reload
Then open http://127.0.0.1:8000/docs to try the routes.
"""

from app.routers import summaries  # noqa: F401  (you will use it)
from fastapi import FastAPI  # noqa: F401  (you will use it)

app = FastAPI(title="Study API", version="0.1.0")

# TODO 5: add the summaries router to the app, with app.include_router(...). Until you do, the
#         /summaries routes do not exist.

# TODO 6: a GET route at "/health" that returns {"status": "ok"}. Use the @app.get decorator on a
#         plain function. A health route tells a load balancer that the process is up.
