from __future__ import annotations

from uuid import UUID
from typing import List, Optional
from abc import ABC, abstractmethod

from app.domain.entities import Group, Student


class BaseGroupPersistence(ABC):
    @abstractmethod
    def get_by_id(self, group_id: UUID) -> Group | None:
        """通过ID获取组"""
        ...

    @abstractmethod
    def get_all(self) -> List[Group]:
        """获取所有组"""
        ...

    @abstractmethod
    def create_group(self, group: Group) -> Group:
        """创建新组"""
        ...

    @abstractmethod
    def delete_group(self, group_id: UUID) -> None:
        """删除组"""
        ...

    @abstractmethod
    def get_all_students(self) -> List[Student]:
        """获取所有学生"""
        ...

    @abstractmethod
    def get_student_by_id(self, student_id: UUID) -> Optional[Student]:
        """通过ID获取学生"""
        ...

    @abstractmethod
    def create_student(self, student: Student) -> Student:
        """创建新学生"""
        ...

    @abstractmethod
    def delete_student(self, student_id: UUID) -> None:
        """删除学生"""
        ...

    @abstractmethod
    def get_group_students(self, group_id: UUID) -> List[Student]:
        """获取组内所有学生"""
        ...

    @abstractmethod
    def assign_student_to_group(self, student_id: UUID, group_id: UUID) -> None:
        """将学生分配到组"""
        ...

    @abstractmethod
    def remove_student_from_group(self, student_id: UUID, group_id: UUID) -> None:
        """从组中移除学生"""
        ...

    @abstractmethod
    def transfer_student_between_groups(self, student_id: UUID, from_group_id: UUID, to_group_id: UUID) -> None:
        """将学生从一个组转移到另一个组"""
        ...

