"""Passwords and tokens: hashing them, and creating and reading JWTs. Module 11 (auth).

Fill in the TODOs, then run the tests. Read the auth lesson, sections 2 and 3, first.
"""


# TODO 16: hash_password(password) returns a hash of the password, never the password itself.
#          Use PasswordHash.recommended() from pwdlib, created once at module level as
#          password_hash. Read the lesson, section 2.
def hash_password(password):
    raise NotImplementedError("TODO 16")


# TODO 16: verify_password(password, hashed) returns True when the password matches the hash.
def verify_password(password, hashed):
    raise NotImplementedError("TODO 16")


# TODO 16: create_access_token(user_id) returns a JWT, signed with the secret key from the
#          settings using the algorithm "HS256". Put the user id in "sub" as a string, and an
#          expiry in "exp", access_token_minutes from now. Use jwt.encode from PyJWT.
#          Read the lesson, section 3.
def create_access_token(user_id):
    raise NotImplementedError("TODO 16")


# TODO 16: read_user_id(token) returns the user id as an int from a valid token. It returns
#          None for a token that is forged, expired, or has a subject that is not a number.
#          Call jwt.decode with the secret key and algorithms=["HS256"], and catch
#          jwt.InvalidTokenError, KeyError and ValueError.
def read_user_id(token):
    raise NotImplementedError("TODO 16")
