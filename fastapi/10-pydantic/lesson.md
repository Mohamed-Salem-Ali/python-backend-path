# Module 10 (FastAPI): Pydantic v2

By the end you can write models that check their data, give readable errors, refuse fields a client should not send, read settings from environment variables, and show every rule in the docs. The project is `fastapi/study-api`.

**Before you start:** finish the FastAPI basics lesson (`../10-basics/lesson.md`). This lesson adds rules to the models you already have.

**Setup:** from `fastapi/study-api`, install the requirements again, because this module adds `pydantic-settings`:

```bash
pip install -r requirements.txt
```

Run this module's tests with `pytest tests/test_validation.py`. All 11 should pass when you finish. Run `pytest` on its own to check the basics as well: 25 tests in all.

**How to read the examples:** the examples use a made-up `notes` app. It is not part of the Study API.

## 1. Pydantic checks the data
A Pydantic model is a class with type hints. Building one from data checks every field:

```python
from pydantic import BaseModel


class Note(BaseModel):
    title: str
    priority: int = 1


Note(title="milk", priority="2")  # Note(title='milk', priority=2): "2" becomes 2
Note(title=5)  # raises ValidationError
```

When a check fails, Pydantic raises `ValidationError`. The error lists every failed field, with its location (`loc`), a message (`msg`) and a type. FastAPI turns that error into a 422 response, which is why the Study API's errors already name the field.

**Try it:** in a Python shell, build `Note(title=5)` inside a `try` block, and print `e.errors()`. Read each key.

## 2. Coercion: lax by default
By default Pydantic converts values that look right. A string `"2"` becomes the integer 2, and `"yes"` becomes `True`. This is convenient for JSON from a form, and it can surprise you. If a field must be a real integer, use `StrictInt`, or `Field(strict=True)`.

**Try it:** build `Note(title="x", priority="2")` and then a strict version of the same model. Compare the two.

## 3. Constraints on fields
`Field` adds rules to a field, and FastAPI shows them in the docs:

```python
from pydantic import BaseModel, Field


class SummaryIn(BaseModel):
    text: str = Field(description="The text to summarise")
    max_words: int = Field(default=50, ge=1, le=500)
```

`ge` is "greater or equal", and `le` is "less or equal". The other common ones are `gt`, `lt`, `min_length`, `max_length` and `pattern`, a regular expression. A value outside a rule gives a 422 with the rule in its message.

The Study API's `max_words` has `ge=1` and `le` set to the limit from settings (section 6). The test `test_the_docs_show_the_limits_of_max_words` checks that the limits reach the OpenAPI spec.

## 4. Your own rules: validators
A rule Pydantic cannot express goes in a validator. A `field_validator` runs for one field and returns the value to keep. Raise `ValueError` to refuse it, and the message becomes part of the error:

```python
from pydantic import BaseModel, field_validator


class NoteIn(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def clean_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("title must not be blank")
        return value
```

Two rules to remember. The validator must return the value, or the field becomes `None`. And Pydantic adds a prefix to the message, so the error reads `Value error, title must not be blank`. A test should check that the text is in the message, not that the whole message matches.

**Try it:** remove the `return value` line from `clean_title` and build `NoteIn(title="milk")`. Read what the field holds afterwards.

## 5. Input and output are different models
One model for everything is a common mistake. The input model says what a client may send. The output model says what a client may see. A stored record often has more fields than either:

```python
class NoteIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str


class NoteOut(BaseModel):
    id: int
    title: str
```

`extra="forbid"` refuses any field the model does not list. In the Study API, a client that sends `owner` gets a 422. This matters: if the input model accepted every field, a client could set its own owner. Keep the rule that the server sets sensitive fields, and the model refuses the rest.

**Try it:** run `pytest tests/test_validation.py::test_an_unknown_field_is_refused_so_clients_cannot_set_the_owner -v`. Find the line that sends the `owner` field.

## 6. Settings from environment variables
A limit that differs between a laptop and a server should not be a number in the code. `BaseSettings` reads it from the environment, converts the text to the right type, and fails at start if the text is wrong:

```python
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="NOTES_")

    max_words: int = 500


def get_settings() -> Settings:
    return Settings()
```

With `env_prefix="NOTES_"`, the variable for `max_words` is `NOTES_MAX_WORDS`. Its value is a string in the environment, and Pydantic converts it to an integer. A value like `lots` raises `ValidationError` when the settings are built.

The Study API uses the prefix `STUDY_`, so its variable is `STUDY_MAX_WORDS`. The commands below use that name. Set the variable for one command. On Windows PowerShell:

```bash
$env:STUDY_MAX_WORDS = "7"
python -c "from app.config import get_settings; print(get_settings().max_words)"
```

On bash:

```bash
STUDY_MAX_WORDS=7 python -c "from app.config import get_settings; print(get_settings().max_words)"
```

Both print `7`. Remove the variable in PowerShell with `Remove-Item Env:STUDY_MAX_WORDS`.

Do not cache the settings. A `functools.lru_cache` on `get_settings` keeps the first value forever, and then a changed variable has no effect until the process restarts. The tests `test_the_limit_comes_from_the_environment` and `test_without_the_environment_the_limit_is_500` change the variable between calls, so a cache fails them. That is the test doing its job.

**Try it:** set the variable to `lots` and run the command above. Read the error. Then remove the variable and run it again.

## 7. The docs show the rules
The OpenAPI spec is built from the models. `Field(ge=1, le=500)` appears in `/openapi.json` as `"minimum": 1` and `"maximum": 500`. A client that builds a form from the spec shows the limits without you writing them twice. The test `test_the_docs_show_the_limits_of_max_words` reads them from the spec.

## 8. Common mistakes
- A validator that does not return the value, so the field becomes `None`.
- Relying on lax coercion without knowing it: `"2"` becomes `2` without an error.
- One model for input and output, so a client can send fields it should not set, or receive fields it should not see.
- Leaving out `extra="forbid"` on input, so unknown fields are silently dropped, or kept if you read them.
- Caching the settings, so a changed environment variable does nothing.
- A list default written as `tags: list[str] = []`. Use `Field(default_factory=list)` so each object gets its own list.

## Exit checklist
- [ ] I can add a `Field` constraint and find it in the docs
- [ ] I can write a validator that trims and refuses a blank value, and say why it must return the value
- [ ] I can explain why the input model refuses unknown fields, using the owner example
- [ ] I can read a setting from an environment variable, and say why the settings are not cached
- [ ] `pytest` passes in `fastapi/study-api`, all 25 tests
