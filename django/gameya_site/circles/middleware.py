"""Middleware: code that runs around every request and every response. Module 07."""

# TODO 23: class RequestIdMiddleware. Django creates one instance when the server starts, and
#          calls it for each request.
#          __init__(self, get_response): store get_response.
#          __call__(self, request):
#            1. Read the X-Request-ID header with request.headers.get("X-Request-ID", ""). The
#               default matters: get() returns None when the header is missing. Keep the id if
#               it is 1 to 64 characters, each an ASCII letter (a-z, A-Z), digit, "-" or "_".
#               Otherwise make a new id with uuid.uuid4().hex, which is 32 hexadecimal characters.
#            2. Store the id as request.request_id, so views and logs can read it.
#            3. Call get_response(request) to run the rest of the stack, then set the header
#               X-Request-ID on the response it returns.
#            4. Return that response.
#          Use re.fullmatch() for the 1-to-64 rule.
