"""Background work: the job that writes flashcards, and the dependency that supplies its maker.

Module 12 (background work): fill in the TODOs. Read the lesson, sections 3, 5 and 6, first.
"""


# TODO 26: get_flashcard_maker() returns the maker: the function in app/flashcards.py that takes
#          a summary's text and returns (front, back) pairs. Routes get it with Depends, and the
#          tests replace it with a fake. Lesson, section 5.
def get_flashcard_maker():
    raise NotImplementedError("TODO 26")


# TODO 26: write_flashcards(summary_id, maker) is the job. It is async, and it runs after the
#          response is sent, so it opens its own session with SessionLocal. Then:
#          - load the Summary, and return if there is none;
#          - run the maker in a worker thread with run_in_threadpool, on summary.summary;
#          - if the maker raises, log the error with logger.exception, and return;
#          - delete the old cards for the summary, add the new ones, and commit, in one
#            transaction. Lesson, sections 3 and 6.
async def write_flashcards(summary_id, maker):
    raise NotImplementedError("TODO 26")


# TODO 32 (a real model and rate limits): change get_flashcard_maker() so it reads the settings:
#          with the provider "stub" it returns the stand-in, as before, and with "gemini" it
#          returns gemini_flashcard_maker(settings) from app/ai.py. The background job does not
#          change. Read the lesson, section 5.
