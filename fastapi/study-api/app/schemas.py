"""The shapes of the data that goes in and out of the API. Module 10: FastAPI basics.

Pydantic reads these classes. A parameter typed as SummaryIn is read from the JSON body, and a
route with response_model=SummaryOut sends back only the fields that SummaryOut lists.
"""

from pydantic import BaseModel


class SummaryIn(BaseModel):
    text: str
    max_words: int = 50


class SummaryOut(BaseModel):
    id: int
    summary: str
    word_count: int
