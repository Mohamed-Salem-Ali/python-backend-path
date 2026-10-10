"""The shapes of the data that goes in and out of the API. Module 10: FastAPI basics, then Pydantic.

Pydantic reads these classes. A parameter typed as SummaryIn is read from the JSON body, and a
route with response_model=SummaryOut sends back only the fields that SummaryOut lists.
"""

from pydantic import BaseModel

# TODO 8 (Pydantic): add the rules to SummaryIn. Read the Pydantic lesson, sections 1 to 5.
#   - text: trim the spaces at both ends, then refuse a blank text with the message
#     "text must not be blank". Do this in a field_validator, and raise ValueError inside it.
#   - max_words: a whole number from 1 up to the limit in app/config.py. Read that limit once,
#     at import time, with get_settings().max_words, into a module constant named MAX_WORDS.
#     Keep the default of 50. Use Field(...) with ge and le, so the limits show in the docs.
#   - Refuse any field that is not listed here: model_config = ConfigDict(extra="forbid").
#     The owner of a summary is set by the server, so a client must not be able to send it.


class SummaryIn(BaseModel):
    text: str
    max_words: int = 50


# TODO 13 (database): the routes now return database rows, not dicts. Give SummaryOut
#         model_config = ConfigDict(from_attributes=True), so Pydantic reads the attributes of a
#         row. Without it, a row is refused as a response.
class SummaryOut(BaseModel):
    id: int
    summary: str
    word_count: int
