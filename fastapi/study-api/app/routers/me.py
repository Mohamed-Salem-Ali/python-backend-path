"""The routes for the signed-in user. Module 11 (auth): fill in the TODOs.

Read the lesson, section 5, first.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/me", tags=["me"])

# TODO 20: GET "" returns the signed-in user as a UserOut. Take user from
#          Depends(get_current_user). With no token, the route answers 401.
# TODO 20: GET "/summaries" returns the summaries whose owner is the signed-in user's
#          username, ordered by id, as a list of SummaryOut. It takes the user from
#          Depends(get_current_user) and the session from Depends(get_session).
