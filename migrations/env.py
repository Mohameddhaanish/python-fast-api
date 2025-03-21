from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.db.session import Base  # Ensure correct import path
from app.db.models import User, Product  # Ensure models are imported

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Debug print to check metadata before assigning
print("Metadata object:", Base.metadata)
print("Tables:", Base.metadata.tables.keys())

target_metadata = Base.metadata  # Assign metadata here

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,  # Ensure this is assigned
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,  # Ensure this is assigned
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()