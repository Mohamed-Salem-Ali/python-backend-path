"""The summaries routes. Module 10 (FastAPI basics): fill in the TODOs, then run the tests.

Run the tests from fastapi/study-api:  pytest
"""

from app import store  # noqa: F401  (you will use it)
from app.schemas import SummaryIn, SummaryOut  # noqa: F401  (you will use these)
from app.summarizer import summarize  # noqa: F401  (you will use it)
from fastapi import APIRouter, HTTPException, Query, Response  # noqa: F401  (you will use these)

# An APIRouter groups routes under one path prefix and one tag. The paths below are written
# relative to the prefix: "" means /summaries, and "/{summary_id}" means /summaries/<id>.
router = APIRouter(prefix="/summaries", tags=["summaries"])

# TODO 1: a POST route with an empty path that takes a SummaryIn body. Answer 201 Created, and
#         declare SummaryOut as the response model. Build a record (a dict) with:
#           "id": store.next_id(), "summary": summarize(...) with the text and max_words,
#           "word_count": the number of words in the text, "owner": "anonymous".
#         Save it in store.SUMMARIES under its id, and return it. The response model leaves
#         "owner" out of the reply.

# TODO 2: a GET route with an empty path. It returns a list of SummaryOut, in id order. Take two
#         query parameters: limit, from 1 to 100, default 20; and offset, 0 or more, default 0.
#         Use Query(...) with ge and le for the limits. Return the records from offset up to
#         offset + limit.

# TODO 3: a GET route at "/{summary_id}", where summary_id is an int. It returns a SummaryOut.
#         If there is no such record, raise HTTPException with status_code 404 and the detail
#         "summary not found".

# TODO 4: a DELETE route at "/{summary_id}". On success it answers 204 No Content and sends no
#         body. If there is no such record, raise HTTPException with status_code 404 and the
#         same detail.

# TODO 11 (database): the four routes above keep their paths, status codes and response models,
#         but they now use the database instead of app/store.py. Each route takes
#         session: AsyncSession = Depends(get_session) and becomes async def. Create: session.add,
#         await session.commit, then await session.refresh. List: await session.scalars with
#         select(Summary), ordered by id, with offset and limit. Fetch: await session.get. Delete:
#         get the row, await session.delete, then await session.commit. The lesson, section 3,
#         shows each call. When no route uses app/store.py any more, delete that file.

# TODO 21 (auth): the create route takes one more parameter: user: User | None =
#         Depends(get_optional_user), from app.dependencies. The owner becomes the user's
#         username, or "anonymous" when no user is signed in. Read the auth lesson, section 7.
