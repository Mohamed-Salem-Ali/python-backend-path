"""The database: one async engine, one session per request, and the base class for the tables.
Module 11 (database): fill in the TODO.

The engine reads its address from the settings (STUDY_DATABASE_URL). FastAPI calls get_session()
for each request, and the route gets a session it can use with await.
"""

from collections.abc import AsyncIterator  # noqa: F401  (you will use it)

from sqlalchemy.ext.asyncio import AsyncSession  # noqa: F401  (you will use it)
from sqlalchemy.orm import DeclarativeBase  # noqa: F401  (you will use it)


class Base:  # TODO 9: make Base a subclass of DeclarativeBase. Every table model inherits it.
    pass


# TODO 9: engine = create_async_engine(get_settings().database_url). Then
#         SessionLocal = async_sessionmaker(engine, expire_on_commit=False).
#         Read the lesson, section 2, for why expire_on_commit is False here.
# TODO 9: async def get_session(): open a session from SessionLocal with async with, and yield
#         it. The session closes itself when the request ends. Its type is
#         AsyncIterator[AsyncSession].
async def get_session():
    raise NotImplementedError("TODO 9")
