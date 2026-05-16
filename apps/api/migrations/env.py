import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from core.config.database import Base
from core.config.settings import get_settings

# Import all models so Alembic can detect them
import modules.auth.infrastructure.models  # noqa: F401
import modules.moderation.infrastructure.models  # noqa: F401
import modules.ai.infrastructure.models  # noqa: F401
import modules.analytics.infrastructure.models  # noqa: F401
import modules.users.infrastructure.models  # noqa: F401
import modules.telegram.infrastructure.models  # noqa: F401
import modules.blacklist.infrastructure.models  # noqa: F401
import modules.audit.infrastructure.models  # noqa: F401

config = context.config
if config.config_file_name:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
settings = get_settings()


def run_migrations_offline() -> None:
    context.configure(
        url=settings.database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    engine = create_async_engine(settings.database_url)
    async with engine.connect() as conn:
        await conn.run_sync(
            lambda sync_conn: context.configure(
                connection=sync_conn,
                target_metadata=target_metadata,
                compare_type=True,
            )
        )
        async with conn.begin():
            await conn.run_sync(lambda _: context.run_migrations())
    await engine.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
