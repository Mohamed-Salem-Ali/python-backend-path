# Module 13 (Django): The capstone

By the end you have one finished project that runs on a real host, with a README that someone else can follow and a short case study you can show a client or an employer.

**Before you start:** finish modules 01 to 12. The capstone is the Gameya project you have built through the course, deployed in module 12.

**What this module is:** a write-up, not new code. You will not add features. You will check what you built, measure it, and explain it. The checks are the test files from modules 02 to 12 and the two checklists in this course: `security-review.md` (module 11) and `deploy-checklist.md` (module 12).

## 1. Freeze the project
Pick one commit as the version you ship. Note its hash. Everything in the write-up refers to that commit.

Run the full set of tests, file by file, and write down the result of each file:

```bash
pytest circles/tests/test_architecture.py
```

Repeat for each test file in `circles/tests/`. A test that fails must be listed with the reason, not hidden. If a feature is missing, say so in the write-up instead of pretending it works.

**Try it:** run `python manage.py check --deploy` with the production variables set, and write down the result. This is the same check as module 11, on the commit you froze.

## 2. Measure it
A case study needs numbers you have measured. Collect these, and note how you measured each one:

- the number of tests that pass, out of the total, for the frozen commit
- the query count of the gameya summary page before and after `select_related` or `prefetch_related` (module 09, `CaptureQueriesContext`)
- the response time of the live home page on the free plan, measured after a warm-up request (module 12, the checklist)
- the number of security review rows that are Pass, Fail, or Open (module 11)

Do not use a number you did not measure. If you did not measure it, leave it out.

## 3. Explain it
You should be able to explain these without notes. Each explanation is a short paragraph, in your own words:

- Why `select_related` removes the N+1 problem, and what it does to the query that runs.
- How a migration works: what `makemigrations` writes, what `migrate` does to the database, and what a rollback would mean for the data.
- Why ownership is checked on the object and again on the new value (module 11).
- Why a token API needs no CSRF token and a session form does (module 11).
- Why the production database comes from `DATABASE_URL` and not from the code (module 12).
- One decision you would make differently now, and why.

If you cannot explain one of these, go back to its module and re-read its section. The write-up should not include anything you could not explain.

## 4. Write the case study
Use `case-study-template.md` in this folder. It has seven headings, with a word limit for each. A case study for a portfolio is short: about 600 words. Keep the numbers from section 2, and the decisions from section 3. Name the live URL and the repository.

## 5. Write the project README
The README is for a stranger who opens the repo. It should answer, in this order:

1. What the project does, in one sentence.
2. Setup: the commands to install the requirements, from a clean clone.
3. Run: the commands to start the app locally, and the URL to open.
4. Test: the command to run the tests, and what a pass means.
5. Deploy: the live URL, and a link to the deploy checklist.
6. What I learned: three to five short points, in your own words.

**Try it:** clone your own repo into a new folder, and follow the README from the first step to the last, without any other notes. Every step that fails is a gap in the README. Fix the README, not the reader.

## 6. Prepare the portfolio entry
The portfolio entry is short: a title, a one-sentence summary, the status (live), the live link, the repository link, and three metrics you measured in section 2. Put the same facts in your CV and profile, and keep the numbers identical across all three.

## 7. Prepare a three-minute talk
Someone may ask you to walk through the project. Prepare three minutes, in this order: the problem, the architecture in one sentence, one decision and its trade-off, one thing that failed and what you did about it, and one thing you would change next. Practise it out loud once.

## Exit checklist
- [ ] The commit I ship is named, and every test file's result is written down
- [ ] Every number in the write-up was measured, and the method is noted
- [ ] I can explain the six items in section 3 without notes
- [ ] The case study uses `case-study-template.md`, and is about 600 words
- [ ] The README passes the clean-clone test in section 5
- [ ] The portfolio entry, the CV and the profile use the same numbers
- [ ] The live URL works, and `deploy-checklist.md` is filled in for this commit

## Common mistakes
- Claiming a feature that a test does not cover.
- Writing a number from memory, instead of measuring it again for the frozen commit.
- Leaving out the failing tests, which makes the rest of the write-up less believable.
- Writing a README that works only on the machine it was written on.
- Using different numbers in the CV, the profile and the case study.
