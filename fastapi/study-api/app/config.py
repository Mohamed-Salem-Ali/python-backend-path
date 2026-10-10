"""Settings read from environment variables. Module 10 (Pydantic): fill in the TODO.

A setting is a value the app needs but should not hard-code: a limit that differs between a laptop
and a server, for example. You set it in the environment, and the code reads it.
"""

# TODO 7: class Settings, a subclass of pydantic_settings.BaseSettings, with one field: max_words,
#         a whole number whose default is 500. Give it a model_config of
#         SettingsConfigDict(env_prefix="STUDY_"), so that the environment variable for max_words
#         is STUDY_MAX_WORDS. Read the lesson, section 6.
#         Then get_settings() returns a new Settings(). It must read the environment on every
#         call, with no cache: the tests change the variable between calls.


class Settings:  # TODO 7: subclass BaseSettings and add the field
    pass


def get_settings():  # TODO 7: return Settings()
    raise NotImplementedError("TODO 7")


# TODO 12 (database): add a second field to Settings: database_url, a text value with the default
#         "sqlite+aiosqlite:///./study.db". With the STUDY_ prefix it is read from
#         STUDY_DATABASE_URL. The engine, the migrations and the tests all read this value.

# TODO 14 (auth): two more fields on Settings, read from the environment the same way.
#         secret_key: text with no default and at least 32 characters, from STUDY_SECRET_KEY.
#         Use Field(min_length=32) and leave out the default, so the app refuses to start
#         without a key. access_token_minutes: a whole number of 1 or more, default 30, from
#         STUDY_ACCESS_TOKEN_MINUTES. Read the auth lesson, sections 3 and 4.
