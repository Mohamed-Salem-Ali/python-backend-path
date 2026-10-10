# Security review: Gameya

Fill in this review for your Gameya project after you finish module 11. For each row, write what you checked and how, and set the result. A row is **Pass** when a test or a command proves it, **Fail** when it does not hold, and **Open** when it is a decision you have not made yet or a risk you accept for now. Do not mark a row Pass because the code looks right.

Date: ____________ Reviewer: ____________ Commit reviewed: ____________

| # | Area | What to check | Proof (test name or command) | Result | Notes |
|---|---|---|---|---|---|
| 1 | Secrets | `SECRET_KEY` comes from the environment in production, with no fallback | `check --deploy` with `DJANGO_PRODUCTION=1` and no key: test `test_production_refuses_to_start_without_a_secret_key` | | |
| 2 | Secrets | No secret is committed to git | `git grep -n "SECRET_KEY\|PASSWORD" -- ':!*.md'` and read every hit | | |
| 3 | Debug | `DEBUG` is off in production | test `test_production_settings_pass_the_django_deploy_checks` | | |
| 4 | Hosts | `ALLOWED_HOSTS` is set from the environment and lists only your domains | the same deploy check | | |
| 5 | HTTPS | Plain HTTP redirects to HTTPS; cookies are sent only over HTTPS; HSTS is on | the same deploy check, plus a browser check after the deploy | | |
| 6 | Auth | An anonymous user cannot change data | `test_an_anonymous_user_cannot_change_a_gameya` | | |
| 7 | Ownership | A user who does not organise a gameya cannot change it | `test_another_user_cannot_change_a_gameya_they_do_not_organise` | | |
| 8 | Ownership | An organiser cannot move a member into a gameya they do not own | `test_an_organiser_cannot_move_a_member_into_someone_elses_gameya` | | |
| 9 | Ownership | Only staff create a gameya | `test_an_organiser_cannot_create_a_gameya` | | |
| 10 | JWT | A wrong password gets no token; a refresh token is refused as an access token; an expired token is refused | the three JWT tests in Part 2 | | |
| 11 | Tokens | Access tokens are short-lived (15 minutes); you accept that a stolen token works until it expires | `SIMPLE_JWT` in settings | | |
| 12 | CSRF | A session form refuses a POST without a CSRF token | `test_a_payment_form_post_without_a_csrf_token_is_refused` | | |
| 13 | XSS | User text (member names) is shown as text | `test_a_member_name_with_a_script_is_shown_as_text` | | |
| 14 | XSS | No template turns escaping off | `test_the_templates_keep_escaping_on` | | |
| 15 | Payments | Who may record a payment? The view accepts a POST from anyone today | **Not covered by a test.** Decide: require a logged-in organiser (and update the tests in `test_class_views.py`), or record this as an open risk | Open | |
| 16 | Login | Too many wrong passwords are slowed or blocked | **Not covered.** Open item unless you add rate limiting | Open | |
| 17 | Passwords | Passwords are stored hashed, and the validators run | `AUTH_PASSWORD_VALIDATORS` in settings; `set_password` in the lesson | | |
| 18 | Dependencies | Packages are pinned to a major version range | `requirements.txt` | | |
| 19 | Errors | Visitors see a plain error page, not a traceback, in production | `DEBUG` off, plus the deploy check | | |
| 20 | Recovery | Password reset works and cannot be guessed | **Not covered.** Open item | Open | |

## Findings

List anything the table does not cover. For each finding, write the risk in one sentence, the fix or the decision, and the test that proves the fix (add one if none exists).

1. 
2. 

## Decisions

Record each decision that you accept as a risk, with the reason and the date you will look at it again.

1. 
