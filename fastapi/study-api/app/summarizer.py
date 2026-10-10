"""A stand-in for an AI call. It keeps the first words and marks the cut with three dots.

Later modules replace this with a real model call, run in the background, so the request does not
wait for it.
"""


def summarize(text: str, max_words: int) -> str:
    words = text.split()
    head = " ".join(words[:max_words])
    return head + "..." if len(words) > max_words else head
