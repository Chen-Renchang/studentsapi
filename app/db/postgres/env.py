from logging.config import fileConfig

from alembic.script import ScriptDirectory
from alembic import context
from sqlmodel import SQLModel
from sqlalchemy import inspect

from app.core.db_config import DB_ENGINE, DB_URI
from app.db.models import *

# Конфигурация Alembic
config = context.config

# Настройка логгера, если указан файл конфигурации
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные для миграций
target_metadata = SQLModel.metadata


def create_tables_if_not_exist():
    """Создает таблицы, если они не существуют."""
    inspector = inspect(DB_ENGINE)
    existing_tables = inspector.get_table_names()  # Получение списка существующих таблиц

    # Получение всех таблиц, определенных в моделях
    defined_tables = SQLModel.metadata.tables

    # Создание таблиц, если они отсутствуют
    for table_name, table in defined_tables.items():
        if table_name not in existing_tables:
            print(f"Создание таблицы: {table_name}")
            table.create(DB_ENGINE)
        else:
            print(f"Таблица {table_name} уже существует.")


def process_revision_directives(context, revision, directives) -> None:  # type: ignore
    """Обработка директив ревизий для автогенерации."""
    if config.cmd_opts and config.cmd_opts.autogenerate:
        script = directives[0]

        # Если изменений нет, пропустить создание ревизии
        if script.upgrade_ops.is_empty():
            directives[:] = []
            print("Изменений не обнаружено.")
        else:
            # Генерация нового идентификатора ревизии
            head_revision = ScriptDirectory.from_config(config).get_current_head()

            if head_revision is None:
                new_rev_id = 1
            else:
                last_rev_id = int(head_revision.lstrip("0"))
                new_rev_id = last_rev_id + 1
            script.rev_id = "{0:04}".format(new_rev_id)


def run_migrations_offline() -> None:
    """Запуск миграций в автономном режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Запуск миграций в онлайн-режиме."""
    try:
        # Сначала попытка создания таблиц напрямую
        create_tables_if_not_exist()
        print("Таблицы успешно созданы!")
    except Exception as e:
        print(f"Ошибка при создании таблиц: {e}")
        print("Переход к выполнению миграций...")

        # Если создание таблиц не удалось, выполнить стандартные миграции
        with DB_ENGINE.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                process_revision_directives=process_revision_directives,
                compare_type=True,
                dialect_opts={"paramstyle": "named"},
            )

            with context.begin_transaction():
                context.run_migrations()


# Запуск миграций в зависимости от режима
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

# Дополнительная проверка для создания таблиц при прямом запуске файла
if __name__ == "__main__":
    create_tables_if_not_exist()
