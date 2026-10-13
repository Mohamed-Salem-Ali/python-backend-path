"""The real model: a small client for the Gemini API, and the makers built on it.

Module 13 (a real model and rate limits): fill in the TODOs. Read the lesson, sections 1 to 5.

The app keeps the stand-ins in app/summarizer.py and app/flashcards.py. The settings decide which
one a request gets: STUDY_AI_PROVIDER=stub (the default) or gemini. Tests never call the real
model: they give httpx2 a fake transport, or replace the maker with a dependency override.
"""

import json  # noqa: F401  (you will use it)

import httpx2  # noqa: F401  (you will use it)

from app.config import get_settings  # noqa: F401  (you will use it)
from app.summarizer import summarize  # noqa: F401  (you will use it)

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


class ModelError(Exception):
    """Raised when the model cannot give a usable answer. The route turns it into a 502."""


# TODO 31: fit_words(text, max_words) returns the text cut to at most max_words words. When it
#          cuts, it adds "..." to the last word, as the stand-in summarizer does. The route uses it
#          because a model does not always keep to the limit you ask for. Lesson, section 4.
def fit_words(text, max_words):
    raise NotImplementedError("TODO 31")


# TODO 31: generate(prompt, settings, *, json_output=False, transport=None) calls the model and
#          returns its answer as text. Lesson, sections 2 and 3.
#          - The body: {"contents": [{"role": "user", "parts": [{"text": prompt}]}],
#            "generationConfig": {"maxOutputTokens": 1024}}. With json_output, also set
#            "responseMimeType": "application/json" in generationConfig.
#          - Send it with POST to GEMINI_URL, with the model from the settings. Put the key in the
#            header "x-goog-api-key", never in the address. The key is a SecretStr, so read it
#            with get_secret_value().
#          - Open the client with httpx2.Client(timeout=settings.ai_timeout_seconds,
#            transport=transport), in a with block. Tests pass a fake transport; the app passes
#            None, which means the real network.
#          - Call raise_for_status(), then read candidates[0].content.parts. Join the "text" of
#            every part that is not a thought (a part with "thought": true).
#          - Turn every failure into ModelError: httpx2.HTTPError (which covers timeouts and bad
#            status codes), and ValueError, KeyError, IndexError and TypeError from a body that
#            is not the expected shape. An answer with no text is a ModelError too.
def generate(prompt, settings, *, json_output=False, transport=None):
    raise NotImplementedError("TODO 31")


# TODO 31: gemini_summarizer(settings, transport=None) returns a function (text, max_words) -> str,
#          with the same shape as summarize() in app/summarizer.py. It builds a prompt that holds
#          the text and asks for at most max_words words, and calls generate. Lesson, section 4.
def gemini_summarizer(settings, transport=None):
    raise NotImplementedError("TODO 31")


# TODO 31: gemini_flashcard_maker(settings, transport=None) returns a function text -> a list of
#          (front, back) pairs, with the same shape as make_flashcards() in app/flashcards.py. It
#          asks for a JSON array of objects with "front" and "back", calls generate with
#          json_output=True, and reads the answer with json.loads. An answer that is not JSON, or
#          an object without "front" or "back", raises ModelError. Lesson, section 4.
def gemini_flashcard_maker(settings, transport=None):
    raise NotImplementedError("TODO 31")


# TODO 32: get_summarizer() is the dependency the create route uses. It reads the settings: with
#          the provider "stub" it returns summarize itself, and with "gemini" it returns
#          gemini_summarizer(settings). Tests replace it with a dependency override. Lesson,
#          section 5.
def get_summarizer():
    raise NotImplementedError("TODO 32")
