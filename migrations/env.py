from logging.config import fileConfig

from alembic import context
from loguru import logger

from app.container import AppContainer
from app.infra.db_models import BaseModel


# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = BaseModel.metadata

APP_CONTAINER = AppContainer()


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    `alembic upgrade <REVISION> --sql`
    """

    context.configure(
        url=APP_CONTAINER.db_settings().url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    engine = APP_CONTAINER.engine()

    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    logger.debug(f"Running migrations in offline mode")
    run_migrations_offline()
else:
    logger.debug(f"Running migrations in online mode")
    run_migrations_online()
