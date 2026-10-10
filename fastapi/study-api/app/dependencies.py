"""Dependencies: functions FastAPI calls before a route, and passes their results to the route.

Module 11 (auth): fill in the TODOs. Read the auth lesson, sections 5 to 7, first.
"""


# TODO 18: oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token"). It reads the token from
#          the header "Authorization: Bearer <token>". Lesson, section 5.
# TODO 18: optional_oauth2_scheme: the same, with auto_error=False, so a missing header gives
#          None instead of a 401. Lesson, section 7.
# TODO 18: _user_from_token(token, session): read the user id with read_user_id, load the User
#          with session.get, and raise HTTPException 401 with the detail
#          "invalid or expired token" and the header WWW-Authenticate: Bearer when there is no
#          user. Lesson, section 5.
# TODO 18: get_current_user(token, session) takes oauth2_scheme and get_session as parameters,
#          with Depends, and returns the user. Lesson, sections 5 and 6.
# TODO 18: get_optional_user(token, session) takes optional_oauth2_scheme and get_session. With
#          no token it returns None; with a token it returns the user, or raises the 401 for a
#          bad token. Lesson, section 7.
async def get_current_user():
    raise NotImplementedError("TODO 18")


async def get_optional_user():
    raise NotImplementedError("TODO 18")
