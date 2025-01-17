from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4


class GroupModel(SQLModel, table=True):
    __tablename__ = "groups"

    id: UUID = Field(primary_key=True)
    name: str
    group_number: str



class StudentModel(SQLModel, table=True):
    __tablename__ = "students"

    id: UUID = Field(primary_key=True)
    name: str
    student_number: str


class GroupStudentModel(SQLModel, table=True):
    __tablename__ = "group_students"

    id: UUID = Field(primary_key=True, default_factory=uuid4)
    group_id: UUID = Field(foreign_key="groups.id")
    student_id: UUID = Field(foreign_key="students.id")
