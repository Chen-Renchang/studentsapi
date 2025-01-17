from uuid import UUID
from typing import List, Optional
from sqlmodel import Session, select

from app.db.models import GroupModel, StudentModel, GroupStudentModel
from app.domain.entities import Group, Student
from app.persistance.base import BaseGroupPersistence


class PostgresGroupPersistence(BaseGroupPersistence):
    def __init__(self, session: Session):
        self.__session = session

    def get_by_id(self, group_id: UUID) -> Optional[Group]:
        """
        Получить группу по её ID.

        Args:
            group_id (UUID): Идентификатор группы.

        Returns:
            Optional[Group]: Объект группы, если она найдена, иначе None.
        """
        query = select(GroupModel).where(GroupModel.id == group_id)
        group = self.__session.exec(query).first()
        if group:
            return Group(id=group.id, name=group.name, number=group.group_number)
        return None

    def get_all(self) -> List[Group]:
        """
        Получить список всех групп.

        Returns:
            List[Group]: Список всех групп.
        """
        query = select(GroupModel)
        groups = self.__session.exec(query).all()
        return [
            Group(id=group.id, name=group.name, number=group.group_number)
            for group in groups
        ]

    def create_group(self, group: Group) -> Group:
        """
        Создать новую группу.

        Args:
            group (Group): Объект группы для создания.

        Returns:
            Group: Созданная группа.
        """
        db_group = GroupModel(
            id=group.id,
            name=group.name,
            group_number=group.number,
        )
        self.__session.add(db_group)
        self.__session.commit()
        self.__session.refresh(db_group)
        return Group(id=db_group.id, name=db_group.name, number=db_group.group_number)

    def delete_group(self, group_id: UUID) -> None:
        """
        Удалить группу по её ID.

        Args:
            group_id (UUID): Идентификатор группы для удаления.
        """
        # Сначала удаляем связи группы со студентами
        query = select(GroupStudentModel).where(GroupStudentModel.group_id == group_id)
        relations = self.__session.exec(query).all()
        for relation in relations:
            self.__session.delete(relation)

        # Затем удаляем саму группу
        query = select(GroupModel).where(GroupModel.id == group_id)
        group = self.__session.exec(query).first()
        if group:
            self.__session.delete(group)
            self.__session.commit()

    def get_all_students(self) -> List[Student]:
        """
        Получить список всех студентов.

        Returns:
            List[Student]: Список всех студентов.
        """
        query = select(StudentModel)
        students = self.__session.exec(query).all()
        return [
            Student(id=student.id, name=student.name, number=student.student_number)
            for student in students
        ]

    def get_student_by_id(self, student_id: UUID) -> Optional[Student]:
        """
        Получить студента по его ID.

        Args:
            student_id (UUID): Идентификатор студента.

        Returns:
            Optional[Student]: Объект студента, если он найден, иначе None.
        """
        query = select(StudentModel).where(StudentModel.id == student_id)
        student = self.__session.exec(query).first()
        if student:
            return Student(id=student.id, name=student.name, number=student.student_number)
        return None

    def create_student(self, student: Student) -> Student:
        """
        Создать нового студента.

        Args:
            student (Student): Объект студента для создания.

        Returns:
            Student: Созданный студент.
        """
        db_student = StudentModel(
            id=student.id,
            name=student.name,
            student_number=student.number
        )
        self.__session.add(db_student)
        self.__session.commit()
        self.__session.refresh(db_student)
        return Student(id=db_student.id, name=db_student.name, number=db_student.student_number)

    def delete_student(self, student_id: UUID) -> None:
        """
        Удалить студента по его ID.

        Args:
            student_id (UUID): Идентификатор студента для удаления.
        """
        # Сначала удаляем связи студента с группами
        query = select(GroupStudentModel).where(GroupStudentModel.student_id == student_id)
        relations = self.__session.exec(query).all()
        for relation in relations:
            self.__session.delete(relation)

        # Затем удаляем самого студента
        query = select(StudentModel).where(StudentModel.id == student_id)
        student = self.__session.exec(query).first()
        if student:
            self.__session.delete(student)
            self.__session.commit()

    def get_group_students(self, group_id: UUID) -> List[Student]:
        """
        Получить список всех студентов в группе.

        Args:
            group_id (UUID): Идентификатор группы.

        Returns:
            List[Student]: Список студентов в группе.
        """
        # Используем JOIN для получения студентов, связанных с группой
        query = (
            select(StudentModel)
            .join(GroupStudentModel)
            .where(GroupStudentModel.group_id == group_id)
        )
        students = self.__session.exec(query).all()
        return [
            Student(id=student.id, name=student.name, number=student.student_number)
            for student in students
        ]

    def assign_student_to_group(self, student_id: UUID, group_id: UUID) -> None:
        """
        Назначить студента в группу.

        Args:
            student_id (UUID): Идентификатор студента.
            group_id (UUID): Идентификатор группы.
        """
        # Проверяем, существует ли уже связь
        query = select(GroupStudentModel).where(
            (GroupStudentModel.student_id == student_id) &
            (GroupStudentModel.group_id == group_id)
        )
        existing = self.__session.exec(query).first()

        if not existing:
            # Создаем новую связь
            relation = GroupStudentModel(student_id=student_id, group_id=group_id)
            self.__session.add(relation)
            self.__session.commit()

    def remove_student_from_group(self, student_id: UUID, group_id: UUID) -> None:
        """
        Удалить студента из группы.

        Args:
            student_id (UUID): Идентификатор студента.
            group_id (UUID): Идентификатор группы.
        """
        query = select(GroupStudentModel).where(
            (GroupStudentModel.student_id == student_id) &
            (GroupStudentModel.group_id == group_id)
        )
        relation = self.__session.exec(query).first()
        if relation:
            self.__session.delete(relation)
            self.__session.commit()

    def transfer_student_between_groups(self, student_id: UUID, from_group_id: UUID, to_group_id: UUID) -> None:
        """
        Перевести студента из одной группы в другую.

        Args:
            student_id (UUID): Идентификатор студента.
            from_group_id (UUID): Идентификатор исходной группы.
            to_group_id (UUID): Идентификатор целевой группы.
        """
        # Удаляем студента из исходной группы
        self.remove_student_from_group(student_id, from_group_id)
        # Добавляем студента в целевую группу
        self.assign_student_to_group(student_id, to_group_id)