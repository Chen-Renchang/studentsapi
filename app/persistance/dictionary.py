from uuid import UUID
from typing import List, Dict
from app.domain.entities import Group, Student
from app.persistance.base import BaseGroupPersistence

# 模拟数据存储
groups: Dict[str, Dict] = {}
students: Dict[str, Dict] = {}
group_students: Dict[str, List[str]] = {}  # 存储组和学生的关系 {group_id: [student_id1, student_id2, ...]}


class GroupDictionaryPersistence(BaseGroupPersistence):
    def get_by_id(self, group_id: UUID) -> Group | None:
        """通过ID获取组"""
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
        """获取所有组"""
        return [
            Group(
                id=UUID(group_dict['id']),
                name=group_dict['name'],
                number=group_dict['number']
            )
            for group_dict in groups.values()
        ]

    def create_group(self, group: Group) -> Group:
        """创建新组"""
        group_str_id = str(group.id)
        groups[group_str_id] = {
            'id': str(group.id),
            'name': group.name,
            'number': group.number
        }
        group_students[group_str_id] = []  # 初始化空的学生列表
        return group

    def delete_group(self, group_id: UUID) -> None:
        """删除组"""
        group_str_id = str(group_id)
        if group_str_id in groups:
            del groups[group_str_id]
            if group_str_id in group_students:
                del group_students[group_str_id]

    def get_all_students(self) -> List[Student]:
        """获取所有学生"""
        return [
            Student(
                id=UUID(student_dict['id']),
                name=student_dict['name'],
                number=student_dict['number']
            )
            for student_dict in students.values()
        ]

    def get_student_by_id(self, student_id: UUID) -> Student | None:
        """通过ID获取学生"""
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
        """创建新学生"""
        student_str_id = str(student.id)
        students[student_str_id] = {
            'id': str(student.id),
            'name': student.name,
            'number': student.number
        }
        return student

    def delete_student(self, student_id: UUID) -> None:
        """删除学生"""
        student_str_id = str(student_id)
        if student_str_id in students:
            # 从所有组中移除该学生
            for group_student_list in group_students.values():
                if student_str_id in group_student_list:
                    group_student_list.remove(student_str_id)
            del students[student_str_id]

    def get_group_students(self, group_id: UUID) -> List[Student]:
        """获取组内所有学生"""
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
        """将学生分配到组"""
        group_str_id = str(group_id)
        student_str_id = str(student_id)

        if group_str_id not in group_students:
            group_students[group_str_id] = []

        if student_str_id not in group_students[group_str_id]:
            group_students[group_str_id].append(student_str_id)

    def remove_student_from_group(self, student_id: UUID, group_id: UUID) -> None:
        """从组中移除学生"""
        group_str_id = str(group_id)
        student_str_id = str(student_id)

        if group_str_id in group_students and student_str_id in group_students[group_str_id]:
            group_students[group_str_id].remove(student_str_id)

    def transfer_student_between_groups(self, student_id: UUID, from_group_id: UUID, to_group_id: UUID) -> None:
        """将学生从一个组转移到另一个组"""
        # 先从原组移除
        self.remove_student_from_group(student_id, from_group_id)
        # 再添加到新组
        self.assign_student_to_group(student_id, to_group_id)
