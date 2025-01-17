from sqlmodel import Session

from app.core.db_config import DB_ENGINE


def session_dependency():
    """Зависимость для создания сессии базы данных."""
    with Session(DB_ENGINE) as session:
        yield session
