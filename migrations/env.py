# migrations/env.py

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import *  # Triggers import of all models


from alembic import context
import os
import sys

# Add app folder to the path so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.base import Base
from database.engine import engine

# Alembic Config object
config = context.config

# Configure loggers from .ini
fileConfig(config.config_file_name)

# Set the target metadata (your models will define this)
target_metadata = Base.metadata

def run_migrations_offline():
    context.configure(
        url=engine.url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
