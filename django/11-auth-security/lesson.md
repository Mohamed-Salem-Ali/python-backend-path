# Module 11 (Django): Auth and security

By the end you can tell authentication from permissions, protect an object so only its owner changes it, issue and check JWTs, explain why a form needs a CSRF token and a token API does not, keep user text escaped in templates, and run Django's deploy checks on production settings.

**Before you start:** finish modules 02 to 10. This module uses the models (02), the forms and views (03 and 04), the templates (05), the DRF API (06), and the pytest fixtures (08).

**Setup:** this module adds `djangorestframework-simplejwt`. From `django/gameya_site`:

```bash
pip install -r requirements.txt
```

Run this module's tests with `pytest circles/tests/test_security.py`. All 19 should pass when you finish. The last two tests start `manage.py` in a new process, so they take a few seconds.

**How to read the examples:** the examples use a made-up `notes` app with one model, `Note` (a title and an owner). It is not part of gameya_site. Learn the pattern, then apply it to Gameya.

## 1. The threats, in one table
Name the threat before you write the defence:

| Threat | In Gameya | Defence | Section |
|---|---|---|---|
| Nobody logged in changes data | an anonymous PATCH to a gameya | authentication, and a 401 | 2, 4 |
| A logged-in user changes someone else's data | a member edits another organiser's gameya | ownership permissions | 4 |
| A malicious page makes the browser send a form | a hidden form posts a payment | CSRF token | 5 |
| User text runs as markup | a member named `<script>...` | auto-escaping | 6 |
| Secrets and debug output leak | DEBUG on, a guessable secret key | secure settings | 7 |

Each row has a test or a deploy check in `test_security.py`. The table is not complete, though. Section 8 asks you to find a threat it leaves out.

## 2. Authentication: who is calling?
Three ways a server knows who is calling:

- **Session:** the server keeps the login state. The browser holds a cookie with an id and sends it with every request to the site, automatically. That automatic sending is what makes CSRF possible (section 5).
- **Token:** the program sends a value in a header, for example `Authorization: Token <key>` (module 06). The server looks the key up in its database. Nothing is sent automatically, so a foreign page cannot use it.
- **JWT (JSON Web Token):** the token carries its own claims, such as the user id and an expiry time, and a signature made with `SECRET_KEY`. The server checks the signature and the expiry, and does not look anything up. The cost: it cannot be revoked before it expires. That is why access tokens are short-lived.

Passwords are never stored as they are. `set_password()` stores a salted hash, and `check_password()` compares. Django's password validators run when a user chooses a password.

**Try it:** in `python manage.py shell`, create a user with `set_password("a-test-password")` and print the first 20 characters of `user.password`. Then print the same field after a second `set_password` with the same password. The two values differ, because each hash has its own salt.

## 3. JWT with simplejwt
Two routes issue and renew tokens. The access token goes in the header on each request:

```python
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("api/jwt/token/", TokenObtainPairView.as_view(), name="api-jwt-token"),
    path("api/jwt/refresh/", TokenRefreshView.as_view(), name="api-jwt-refresh"),
]
```

A client logs in once, then sends the access token. Replace the placeholders with real values:

```bash
curl -X POST http://127.0.0.1:8000/api/jwt/token/ -H "Content-Type: application/json" -d '{"username": "<user>", "password": "<password>"}'
```

```bash
curl -X PATCH http://127.0.0.1:8000/api/gameyas/1/ -H "Authorization: Bearer <access token>" -H "Content-Type: application/json" -d '{"name": "Renamed"}'
```

The API checks three things on every request: the signature, the expiry, and the token type. A refresh token has type `refresh`, so the API refuses it as an access token. The lifetimes limit the damage from a theft: a stolen access token works for 15 minutes, and a stolen refresh token works for a week, so it must never leave the client.

The lifetimes and the header word live in one dictionary, `SIMPLE_JWT`. The JWT signature uses `SECRET_KEY`, so a short key is a weak signature. simplejwt warns when the key is shorter than 32 bytes. Keep the key long.

**Try it:** open `test_an_expired_access_token_is_refused` and find the line that makes the token expired. Explain why the API answers 401 and not 403.

## 4. Authorization: what may this user do?
Two checks run for each request, in DRF:

- `has_permission(request, view)` runs before the view. It does not see an object. Use it for "may this user make this kind of request at all?", such as "only staff create a gameya".
- `has_object_permission(request, view, obj)` runs after the view loads the object (`get_object()`). Use it for "may this user touch this row?".

Warning: `BasePermission.has_object_permission` returns `True` by default. A permission class that checks only `has_permission` lets every logged-in user change every row. This is the most common ownership bug in DRF.

The owner check, for the made-up `Note` model with an `owner` field:

```python
class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner_id == request.user.id
```

For Gameya, the owner is `organiser`. Staff may change anything. A member is owned through its gameya, so the check looks at `obj.gameya` for a member and at `obj` for a gameya.

**Check the target, not only the object.** An organiser may change a member they own. If the organiser can also send `"gameya": <another id>` in the same PATCH, the member moves into a gameya they do not own. The object check passes, because the member was theirs before the change. The fix runs in `perform_update`, where the new value is known: check the new gameya the same way (TODO 41, and `test_an_organiser_cannot_move_a_member_into_someone_elses_gameya`).

**Try it:** in a scratch copy of the project, delete the line `return gameya.organiser_id == request.user.id` and run `pytest circles/tests/test_security.py`. Count the tests that fail, and explain each one.

## 5. CSRF: a forged form post
Your browser sends the session cookie with every request to the site, including a request that another page triggers. A malicious page can make your browser post to a form on the site. Without a defence, the site cannot tell that post from one you chose to make.

The defence is a secret token that the form carries and the attacker cannot read. A page on another site cannot read your pages, because of the browser's same-origin rule. Django's `CsrfViewMiddleware` checks the token on every POST, unless the view is marked `csrf_exempt`. A form gets the token from `{% csrf_token %}` (module 05).

Two rules follow:

- A token API that uses `Authorization` headers needs no CSRF token. The browser does not add that header by itself, so a foreign page cannot send it. This is why the tests can write through the API without a token.
- A session-based form needs the token. DRF's `SessionAuthentication` checks it too.

Gameya's payment form (module 04, `GameyaPayments`) is session-style and checks the token. A POST without it gets a 403. The test `test_a_payment_form_post_without_a_csrf_token_is_refused` shows that.

Be careful with the other part of this: the same view accepts a payment from anyone, logged in or not. The CSRF check does not fix that. Section 8 asks you to decide what to do about it.

**Try it:** read `test_a_payment_form_post_with_the_csrf_token_is_accepted`. Find where the token comes from, and explain why the admin login page is a convenient real form to read it from.

## 6. XSS: user text turned into markup
Django escapes `<`, `>`, `&`, `"` and `'` in `{{ value }}`. So a member named `<script>...` appears on the page as text, not as a script.

```python
from django.template import Context, Template

Template("{{ name }}").render(Context({"name": "<b>hi</b>"}))
# '&lt;b&gt;hi&lt;/b&gt;'
```

Escaping does not protect everything. Four cases need care:

- `|safe` and `mark_safe()` tell Django that the text is already safe. Use them only on text your code made.
- `{% autoescape off %}` switches escaping off for a whole block.
- Inside a `<script>` block, do not write `{{ value }}`. Use the `json_script` filter: `{{ data|json_script:"notes-data" }}`.
- In an `href` or `src`, escaping does not stop a `javascript:` address. Accept only `http` and `https` links.

The tests check two things: the page shows the script as text, and the template files contain no `|safe` and no `autoescape off`.

**Try it:** change the member name in `test_a_member_name_with_a_script_is_shown_as_text` to a link with a `javascript:` address. Does the test still pass? Explain what that tells you about escaping.

## 7. Secure settings
Each setting protects one thing:

- **SECRET_KEY** signs sessions, JWTs and password-reset links. It must not be in git. Production reads it from the environment and has no fallback.
- **DEBUG** shows full tracebacks and settings to any visitor. Off in production.
- **ALLOWED_HOSTS** lists the host names the site answers to. Set it from the environment.
- **HTTPS settings:** `SECURE_SSL_REDIRECT` sends plain HTTP to HTTPS. `SESSION_COOKIE_SECURE` and `CSRF_COOKIE_SECURE` send the cookies only over HTTPS. `SECURE_HSTS_SECONDS` tells the browser to use HTTPS only for that long. Start at an hour while you test a deploy. Raise it to one year (31536000) when every subdomain serves HTTPS. `SECURE_HSTS_INCLUDE_SUBDOMAINS` and `SECURE_HSTS_PRELOAD` extend the same promise. The preload list is a separate submission, so setting `SECURE_HSTS_PRELOAD` does not add the site to it.
- **SECURE_PROXY_SSL_HEADER** matters behind a host such as Render. The host ends HTTPS and forwards plain HTTP. This header tells Django the original request was HTTPS, so the redirect and the secure cookies work.

Django checks all of this for you:

```bash
python manage.py check --deploy
```

Generate a secret key of 50 or more characters:

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Run the deploy check with production settings. On Windows PowerShell, set the variables with `$env:DJANGO_PRODUCTION = "1"` and the other two the same way first. Then run the check:

```bash
DJANGO_PRODUCTION=1 DJANGO_SECRET_KEY="<the key you generated>" DJANGO_ALLOWED_HOSTS=gameya.example.com python manage.py check --deploy
```

**Try it:** run the same check without `DJANGO_SECRET_KEY`. Read the message. Then find the test that expects this message.

## 8. Project step: the security review
Open `security-review.md` in this folder. For each row, write what you checked and how. A row is done when a test or a command proves it. Some rows are not covered by any test: the review should say so.

The most important row is the payment form. The view from module 04 accepts a payment from an anonymous visitor. Look at the tests in `test_class_views.py`: they post without logging in, so requiring a login changes those tests too. Write down your decision: fix it now and update those tests, or record it as an open risk. Either answer is acceptable in a review, as long as it is written down.

Rate limiting (too many login attempts) and password reset are not covered by this module. List them as open items.

## Exit checklist
- [ ] I can say how a session, a token and a JWT differ, and which one a browser form uses
- [ ] I can name the two DRF permission checks, and say which one sees the object
- [ ] I can explain why a token API needs no CSRF token, and a form does
- [ ] I can name three cases where escaping does not protect a page
- [ ] `pytest circles/tests/test_security.py` passes, all 19 tests
- [ ] `check --deploy` with the production variables reports no issues
- [ ] `security-review.md` is filled in for the Gameya project, with open items listed

## Common mistakes
- Forgetting `has_object_permission`. The default returns `True`, so every logged-in user can change every row.
- Checking the object but not the new value that moves it to another owner.
- Using `|safe` on user text to fix a display problem.
- Long-lived access tokens. A stolen JWT works until it expires, and this module does not revoke tokens.
- Putting `SECRET_KEY` in git, or in a file you deploy.
- Turning `DEBUG` on in production because it helps with a bug.
