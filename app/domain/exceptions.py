from uuid import UUID

class GroupNotFoundException(Exception):
    def __init__(self, group_id: UUID):
        self.group_id = group_id
        super().__init__(f"Group with id {group_id} not found")

class StudentNotFoundException(Exception):
    def __init__(self, student_id: UUID):
        self.student_id = student_id
        super().__init__(f"Student with id {student_id} not found")

class StudentAlreadyInGroupException(Exception):
    def __init__(self, student_id: UUID, group_id: UUID):
        self.student_id = student_id
        self.group_id = group_id
        super().__init__(
            f"Student {student_id} is already in group {group_id}"
        )
