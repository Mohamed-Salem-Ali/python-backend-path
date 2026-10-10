# Case study: Gameya (template)

Copy this file into your own portfolio repo, and fill in each heading. The word limits are guides for about 600 words in all. Replace every line in italics with your own text. Delete the italic guidance when you are done.

**Live:** _(URL from the deploy checklist)_ **Repository:** _(URL)_ **Commit shipped:** _(hash)_

## 1. The problem (about 80 words)
_Who uses this, and what problem did a rotating savings circle have before this app? Name one concrete situation, such as a missed payment or an unclear payout turn._

## 2. What it does (about 100 words)
_List the main things a user can do, in short sentences. Say what a visitor can see without logging in, and what an organiser can change._

## 3. How it is built (about 120 words)
_Describe the parts in order: the models, the API, the templates, the background task, the deploy. Name the tools (Django, DRF, Celery, PostgreSQL, WhiteNoise, gunicorn, Render). One sentence per part._

## 4. Decisions and trade-offs (about 120 words)
_Pick two decisions. For each: what you chose, what you did not choose, and what it costs. Example: JWT for the API, which cannot be revoked before it expires, so access tokens last 15 minutes._

## 5. Security (about 80 words)
_Summarise the security review: how many rows passed, failed, and stayed open. Name one open risk and say what you would do about it. Do not describe a weakness in a way that helps an attacker, and do not include any secret._

## 6. Measured results (about 60 words)
_Give the numbers you measured for the frozen commit, and how you measured each one. Example: the summary page went from 53 queries to 3 with select_related, measured with CaptureQueriesContext._

## 7. What I would change next (about 40 words)
_One or two things, and why. Be specific: a feature, a test, or a deploy setting._

---

**Checklist before you publish:** the live link opens over HTTPS; the repo README passes a clean-clone test; every number matches the frozen commit; no secret, password, or personal data appears in the text.
