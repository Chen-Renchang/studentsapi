from logging.config import fileConfig

from alembic.script import ScriptDirectory
from alembic import context
from sqlmodel import SQLModel
from sqlalchemy import inspect

from app.core.db_config import DB_ENGINE, DB_URI
from app.db.models import *

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def create_tables_if_not_exist():
    """直接创建不存在的表"""
    inspector = inspect(DB_ENGINE)
    existing_tables = inspector.get_table_names()

    # 获取所有模型定义的表
    defined_tables = SQLModel.metadata.tables

    # 创建不存在的表
    for table_name, table in defined_tables.items():
        if table_name not in existing_tables:
            print(f"Creating table: {table_name}")
            table.create(DB_ENGINE)
        else:
            print(f"Table {table_name} already exists")


def process_revision_directives(context, revision, directives) -> None:  # type: ignore
    if config.cmd_opts and config.cmd_opts.autogenerate:
        script = directives[0]

        if script.upgrade_ops.is_empty():
            directives[:] = []
            print("No changes detected.")
        else:
            head_revision = ScriptDirectory.from_config(config).get_current_head()

            if head_revision is None:
                new_rev_id = 1
            else:
                last_rev_id = int(head_revision.lstrip("0"))
                new_rev_id = last_rev_id + 1
            script.rev_id = "{0:04}".format(new_rev_id)


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
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
    """Run migrations in 'online' mode."""
    try:
        # 首先尝试直接创建表
        create_tables_if_not_exist()
        print("Tables created successfully!")
    except Exception as e:
        print(f"Error creating tables: {e}")
        print("Falling back to migrations...")

        # 如果创建表失败，继续执行正常的迁移流程
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


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

# 如果你想在文件执行时直接创建表，可以添加这个条件
if __name__ == "__main__":
    create_tables_if_not_exist()
