from uuid import UUID
from typing import List, Dict
from app.domain.entities import Group, Student
from app.persistance.base import BaseGroupPersistence

# Имитация хранения данных в памяти
groups: Dict[str, Dict] = {}  # Словарь для хранения групп
students: Dict[str, Dict] = {}  # Словарь для хранения студентов
group_students: Dict[str, List[str]] = {}  # Словарь для хранения связей групп и студентов {group_id: [student_id1, student_id2, ...]}


class GroupDictionaryPersistence(BaseGroupPersistence):
    def get_by_id(self, group_id: UUID) -> Group | None:
        """Получить группу по ID."""
        group_str_id = str(group_id)
        if group_str_id in groups:
            group_dict = groups[group_str_id]
            return Group(
                id=UUID(group_dict['id']),
                name=group_dict['name'],
                number=group_dict['number']
            )
        return None

    def get_all(self) -> List[Group]:
        """Получить все группы."""
        return [
            Group(
                id=UUID(group_dict['id']),
                name=group_dict['name'],
                number=group_dict['number']
            )
            for group_dict in groups.values()
        ]

    def create_group(self, group: Group) -> Group:
        """Создать новую группу."""
        group_str_id = str(group.id)
        groups[group_str_id] = {
            'id': str(group.id),
            'name': group.name,
            'number': group.number
        }
        group_students[group_str_id] = []  # Инициализация пустого списка студентов
        return group

    def delete_group(self, group_id: UUID) -> None:
        """Удалить группу."""
        group_str_id = str(group_id)
        if group_str_id in groups:
            del groups[group_str_id]
            if group_str_id in group_students:
                del group_students[group_str_id]

    def get_all_students(self) -> List[Student]:
        """Получить всех студентов."""
        return [
            Student(
                id=UUID(student_dict['id']),
                name=student_dict['name'],
                number=student_dict['number']
            )
            for student_dict in students.values()
        ]

    def get_student_by_id(self, student_id: UUID) -> Student | None:
        """Получить студента по ID."""
        student_str_id = str(student_id)
        if student_str_id in students:
            student_dict = students[student_str_id]
            return Student(
                id=UUID(student_dict['id']),
                name=student_dict['name'],
                number=student_dict['number']
            )
        return None

    def create_student(self, student: Student) -> Student:
        """Создать нового студента."""
        student_str_id = str(student.id)
        students[student_str_id] = {
            'id': str(student.id),
            'name': student.name,
            'number': student.number
        }
        return student

    def delete_student(self, student_id: UUID) -> None:
        """Удалить студента."""
        student_str_id = str(student_id)
        if student_str_id in students:
            # Удаление студента из всех групп
            for group_student_list in group_students.values():
                if student_str_id in group_student_list:
                    group_student_list.remove(student_str_id)
            del students[student_str_id]

    def get_group_students(self, group_id: UUID) -> List[Student]:
        """Получить всех студентов в группе."""
        group_str_id = str(group_id)
        if group_str_id in group_students:
            student_ids = group_students[group_str_id]
            return [
                Student(
                    id=UUID(students[student_id]['id']),
                    name=students[student_id]['name'],
                    number=students[student_id]['number']
                )
                for student_id in student_ids
                if student_id in students
            ]
        return []

    def assign_student_to_group(self, student_id: UUID, group_id: UUID) -> None:
        """Добавить студента в группу."""
        group_str_id = str(group_id)
        student_str_id = str(student_id)

        if group_str_id not in group_students:
            group_students[group_str_id] = []

        if student_str_id not in group_students[group_str_id]:
            group_students[group_str_id].append(student_str_id)

    def remove_student_from_group(self, student_id: UUID, group_id: UUID) -> None:
        """Удалить студента из группы."""
        group_str_id = str(group_id)
        student_str_id = str(student_id)

        if group_str_id in group_students and student_str_id in group_students[group_str_id]:
            group_students[group_str_id].remove(student_str_id)

    def transfer_student_between_groups(self, student_id: UUID, from_group_id: UUID, to_group_id: UUID) -> None:
        """Переместить студента из одной группы в другую."""
        # Сначала удаляем из исходной группы
        self.remove_student_from_group(student_id, from_group_id)
        # Затем добавляем в новую группу
        self.assign_student_to_group(student_id, to_group_id)
