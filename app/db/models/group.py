from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4


class GroupModel(SQLModel, table=True):
    """Модель группы."""
    __tablename__ = "groups"  # Название таблицы в базе данных

    id: UUID = Field(primary_key=True)  # Уникальный идентификатор группы (первичный ключ)
    name: str  # Название группы
    group_number: str  # Номер группы


class StudentModel(SQLModel, table=True):
    """Модель студента."""
    __tablename__ = "students"  # Название таблицы в базе данных

    id: UUID = Field(primary_key=True)  # Уникальный идентификатор студента (первичный ключ)
    name: str  # Имя студента
    student_number: str  # Номер студента


class GroupStudentModel(SQLModel, table=True):
    """Модель для связи студентов и групп."""
    __tablename__ = "group_students"  # Название таблицы в базе данных

    id: UUID = Field(primary_key=True, default_factory=uuid4)  # Уникальный идентификатор связи (первичный ключ)
    group_id: UUID = Field(foreign_key="groups.id")  # Внешний ключ на таблицу групп
    student_id: UUID = Field(foreign_key="students.id")  # Внешний ключ на таблицу студентов
