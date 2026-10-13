"""The sign-up and login routes. Module 11 (auth): fill in the TODOs.

Routes: POST /auth/register and POST /auth/token. Read the lesson, section 4, first.
"""

from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

# TODO 19: POST "/register" takes a UserIn and answers 201 Created with a UserOut. Hash the
#          password with run_in_threadpool, so the event loop is not blocked, and save the User.
#          If the username is taken, the commit raises IntegrityError: roll back, and raise
#          HTTPException 409 with the detail "username already taken".
# TODO 19: POST "/token" takes the form OAuth2PasswordRequestForm, from Depends(). Find the user
#          by username. Check the password with verify_password, also in run_in_threadpool.
#          An unknown user and a wrong password both raise HTTPException 401 with the detail
#          "incorrect username or password" and the header WWW-Authenticate: Bearer. Otherwise
#          return a Token with create_access_token(user.id).

# TODO 35 (a real model and rate limits): add dependencies=[Depends(rate_limit)] to the "/token"
#          route, so a password cannot be guessed as fast as the server answers. Register is not
#          limited here. Read the lesson, section 7.
