from __future__ import annotations

from uuid import UUID
from typing import List, Optional
from abc import ABC, abstractmethod

from app.domain.entities import Group, Student


class BaseGroupPersistence(ABC):
    @abstractmethod
    def get_by_id(self, group_id: UUID) -> Group | None:
        """Получить группу по ID."""
        ...

    @abstractmethod
    def get_all(self) -> List[Group]:
        """Получить все группы."""
        ...

    @abstractmethod
    def create_group(self, group: Group) -> Group:
        """Создать новую группу."""
        ...

    @abstractmethod
    def delete_group(self, group_id: UUID) -> None:
        """Удалить группу."""
        ...

    @abstractmethod
    def get_all_students(self) -> List[Student]:
        """Получить всех студентов."""
        ...

    @abstractmethod
    def get_student_by_id(self, student_id: UUID) -> Optional[Student]:
        """Получить студента по ID."""
        ...

    @abstractmethod
    def create_student(self, student: Student) -> Student:
        """Создать нового студента."""
        ...

    @abstractmethod
    def delete_student(self, student_id: UUID) -> None:
        """Удалить студента."""
        ...

    @abstractmethod
    def get_group_students(self, group_id: UUID) -> List[Student]:
        """Получить всех студентов в группе."""
        ...

    @abstractmethod
    def assign_student_to_group(self, student_id: UUID, group_id: UUID) -> None:
        """Добавить студента в группу."""
        ...

    @abstractmethod
    def remove_student_from_group(self, student_id: UUID, group_id: UUID) -> None:
        """Удалить студента из группы."""
        ...

    @abstractmethod
    def transfer_student_between_groups(self, student_id: UUID, from_group_id: UUID, to_group_id: UUID) -> None:
        """Переместить студента из одной группы в другую."""
        ...
