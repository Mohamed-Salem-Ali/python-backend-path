"""A stand-in for the AI call that writes flashcards. Module 12 (background work).

It makes one card per sentence, and it stays the default. The real version, in app/ai.py
(module 13), calls a model. The background job does not change when that happens, because the job
only needs a function that takes text and returns (front, back) pairs.
"""


def make_flashcards(text: str) -> list[tuple[str, str]]:
    sentences = [part.strip() for part in text.split(".") if part.strip()]
    return [(f"Recall the sentence that starts with '{s.split()[0]}'", s) for s in sentences]
