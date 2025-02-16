from alembic import context
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
import asyncio
import os
import sys

# Добавляем путь к проекту
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "src")))

# Импортируем настройки
from settings import AppSettings

from models.models import UsersModel, PostsModel
# Импортируем базовый класс моделей
from db.core import ModelBase

target_metadata = ModelBase.metadata

def run_migrations_online():
    """
    Асинхронный запуск миграций в режиме 'online'.
    """
    connectable = context.config.attributes.get("connection", None)

    if connectable is None:
        # Используем URL из настроек напрямую
        connectable = create_async_engine(
            AppSettings.db_url,
            poolclass=pool.NullPool,
        )

    async def run_async_migrations():
        async with connectable.connect() as connection:
            await connection.run_sync(do_run_migrations)

    asyncio.run(run_async_migrations())

def do_run_migrations(connection):
    """
    Запуск миграций с указанным соединением.
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True
    )

    with context.begin_transaction():
        context.run_migrations()

if context.is_offline_mode():
    raise NotImplementedError("Асинхронные миграции не поддерживаются в offline-режиме")
else:
    run_migrations_online()