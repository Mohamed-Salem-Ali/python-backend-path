"""A stand-in for an AI call. It keeps the first words and marks the cut with three dots.

The course keeps this stand-in, so the project runs with no API key. Replacing it with a real model
call is a stretch goal; see the advanced tier in fastapi/SYLLABUS.md.
"""


def summarize(text: str, max_words: int) -> str:
    words = text.split()
    head = " ".join(words[:max_words])
    return head + "..." if len(words) > max_words else head
