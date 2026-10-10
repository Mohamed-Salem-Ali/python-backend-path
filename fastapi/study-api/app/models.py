"""The database tables. Module 11 (database): one model, Summary, for the summaries table.

Write the model, then run the migration commands in the lesson (sections 3 to 5).
"""

from app.database import Base  # noqa: F401  (you will use it)


class Summary:  # TODO 10: subclass Base, and set __tablename__ = "summaries".
    # Add these columns, with Mapped[...] type hints and mapped_column(...):
    #   id          int, the primary key
    #   summary     text
    #   word_count  int
    #   owner       text, default "anonymous"
    #   created_at  a datetime that the database sets when the row is inserted:
    #               server_default=func.now()
    # Then, after section 5 of the lesson, add the language column:
    #   language    text, up to 8 characters, default "en" in the database too.
    pass


class User:  # TODO 15: subclass Base, and set __tablename__ = "users". Add these columns:
    #   id             int, the primary key
    #   username       text, up to 50 characters, unique
    #   password_hash  text, up to 255 characters
    # Read the auth lesson, section 4. Then run the migration commands in that section.
    pass
