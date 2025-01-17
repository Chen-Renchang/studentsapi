from pydantic import PostgresDsn
from sqlmodel import create_engine

from app.core.config import SETTINGS

# Вывод настроек для проверки
print(SETTINGS)

# Создание URI для подключения к PostgreSQL
DB_URI = f"postgresql://{SETTINGS.DB_USER}:{SETTINGS.DB_PASSWORD}@{SETTINGS.DB_HOSTNAME}:{SETTINGS.DB_PORT}/{SETTINGS.DB_NAME}"

# Создание движка базы данных с использованием SQLModel
DB_ENGINE = create_engine(DB_URI)
