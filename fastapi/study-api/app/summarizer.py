"""A stand-in for an AI call. It keeps the first words and marks the cut with three dots.

It stays the default, so the project runs with no API key. The bonus module 13 adds a real model
call in app/ai.py, and the setting STUDY_AI_PROVIDER chooses between the two.
"""


def summarize(text: str, max_words: int) -> str:
    words = text.split()
    head = " ".join(words[:max_words])
    return head + "..." if len(words) > max_words else head
