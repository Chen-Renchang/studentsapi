from uuid import UUID
from pydantic import BaseModel
from typing import List, Optional

# Базовые схемы
class ApiV1GroupCreateSchema(BaseModel):
    id: UUID
    name: str
    number: str

class ApiV1GroupGetSchema(BaseModel):
    id: UUID
    name: str
    number: str

class ApiV1StudentCreateSchema(BaseModel):
    id: UUID
    name: str
    number: str

class ApiV1StudentGetSchema(BaseModel):
    id: UUID
    name: str
    number: str
    group_id: Optional[UUID] = None  # Студент может принадлежать к группе

# Схемы для списков
class ApiV1GroupListSchema(BaseModel):
    groups: List[ApiV1GroupGetSchema]

class ApiV1StudentListSchema(BaseModel):
    students: List[ApiV1StudentGetSchema]

# Схемы для ответов на удаление
class ApiV1StudentDeleteResponseSchema(BaseModel):
    success: bool
    message: str
    student_id: UUID

class ApiV1GroupDeleteResponseSchema(BaseModel):
    success: bool
    message: str
    group_id: UUID

# Схемы для операций с группами студентов
class ApiV1StudentGroupAssignSchema(BaseModel):
    student_id: UUID
    group_id: UUID

class ApiV1StudentGroupRemoveSchema(BaseModel):
    student_id: UUID
    group_id: UUID

class ApiV1StudentGroupTransferSchema(BaseModel):
    student_id: UUID
    from_group_id: UUID
    to_group_id: UUID

# Схема для списка студентов в группе
class ApiV1GroupStudentsSchema(BaseModel):
    group_id: UUID
    group_name: str
    students: List[ApiV1StudentGetSchema]
