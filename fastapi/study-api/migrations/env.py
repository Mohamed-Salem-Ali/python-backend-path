"""Alembic reads this file for each migration command: upgrade, downgrade and revision.

It uses the same database address as the app (STUDY_DATABASE_URL), and it imports the models so
that autogenerate can compare them with the database. You do not need to change this file.
"""

import asyncio

from alembic import context
from app import models  # noqa: F401  (registers the models on Base.metadata)
from app.config import get_settings
from app.database import Base
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config

config = context.config
config.set_main_option("sqlalchemy.url", get_settings().database_url)
target_metadata = Base.metadata


def run_migrations_on(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        # SQLite cannot change a column in place. Batch mode rebuilds the table instead.
        render_as_batch=True,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    engine = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with engine.connect() as connection:
        await connection.run_sync(run_migrations_on)
    await engine.dispose()


asyncio.run(run_async_migrations())
