import sys
import os
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 1. IMPORT YOUR APP'S CONFIG AND MODELS HERE
from app.core.config import settings
from app.models.transactions import Base

config = context.config

# 2. INJECT YOUR DATABASE URL FROM .ENV
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 3. SET THE TARGET METADATA
target_metadata = Base.metadata