from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from typing import Optional

from app.api.v1.schemas.group import (
    ApiV1GroupGetSchema,
    ApiV1GroupCreateSchema,
    ApiV1GroupListSchema,
    ApiV1GroupDeleteResponseSchema,
    ApiV1GroupStudentsSchema,
    ApiV1StudentCreateSchema,
    ApiV1StudentGetSchema,
    ApiV1StudentListSchema,
    ApiV1StudentDeleteResponseSchema,
    ApiV1StudentGroupAssignSchema,
    ApiV1StudentGroupRemoveSchema,
    ApiV1StudentGroupTransferSchema
)
from app.core.dependencies.group import group_persistence_dependency
from app.domain.entities import Group, Student
from app.persistance.base import BaseGroupPersistence

router = APIRouter()


# Эндпоинты для работы с группами
@router.get("/groups", summary="Get all groups", response_model=ApiV1GroupListSchema)
async def get_groups(
        group_persistence: BaseGroupPersistence = Depends(group_persistence_dependency)
) -> ApiV1GroupListSchema:
    """Получить список всех групп (требование 8)"""
    groups = group_persistence.get_all()
    return ApiV1GroupListSchema(
        groups=[ApiV1GroupGetSchema(id=g.id, name=g.name, number=g.number) for g in groups]
    )


@router.get("/groups/{group_id}", summary="Get group by ID", response_model=Optional[ApiV1GroupGetSchema])
async def get_group(
        group_id: UUID,
        group_persistence: BaseGroupPersistence = Depends(group_persistence_dependency)
) -> Optional[ApiV1GroupGetSchema]:
    """Получить информацию о группе по её ID (требование 4)"""
    group = group_persistence.get_by_id(group_id)
    if group:
        return ApiV1GroupGetSchema(id=group.id, name=group.name, number=group.number)
    return None


@router.post("/groups", summary="Create new group", response_model=ApiV1GroupGetSchema)
async def create_group(
        group_to_create: ApiV1GroupCreateSchema,
        group_persistence: BaseGroupPersistence = Depends(group_persistence_dependency)
) -> ApiV1GroupCreateSchema:
    """Создать новую группу (требование 2)"""
    group = Group(
        id=group_to_create.id,
        name=group_to_create.name,
        number=group_to_create.number
    )
    created_group = group_persistence.create_group(group)
    return ApiV1GroupCreateSchema(
        id=created_group.id,
        name=created_group.name,
        number=created_group.number
    )


@router.delete("/groups/{group_id}", summary="Delete group", response_model=ApiV1GroupDeleteResponseSchema)
async def delete_group(
        group_id: UUID,
        group_persistence: BaseGroupPersistence = Depends(group_persistence_dependency)
) -> ApiV1GroupDeleteResponseSchema:
    """Удалить группу (требование 6)"""
    if not group_persistence.get_by_id(group_id):
        raise HTTPException(status_code=404, detail="Group not found")

    group_persistence.delete_group(group_id)
    return ApiV1GroupDeleteResponseSchema(
        success=True,
        message="Group successfully deleted",
        group_id=group_id
    )


# Эндпоинты для работы со студентами
@router.get("/students", summary="Get all students", response_model=ApiV1StudentListSchema)
async def get_students(
        group_persistence: BaseGroupPersistence = Depends(group_persistence_dependency)
) -> ApiV1StudentListSchema:
    """Получить список всех студентов (требование 7)"""
    students = group_persistence.get_all_students()
    return ApiV1StudentListSchema(
        students=[
            ApiV1StudentGetSchema(
                id=student.id,
                name=student.name,
                number=student.number
            ) for student in students
        ]
    )


@router.get("/students/{student_id}", summary="Get student by ID", response_model=ApiV1StudentGetSchema)
async def get_student(
        student_id: UUID,
        group_persistence: BaseGroupPersistence = Depends(group_persistence_dependency)
) -> ApiV1StudentGetSchema:
    """Получить информацию о студенте по его ID (требование 3)"""
    student = group_persistence.get_student_by_id(student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return ApiV1StudentGetSchema(
        id=student.id,
        name=student.name,
        number=student.number
    )


@router.post("/students", summary="Create new student", response_model=ApiV1StudentGetSchema)
async def create_student(
        student: ApiV1StudentCreateSchema,
        group_persistence: BaseGroupPersistence = Depends(group_persistence_dependency)
) -> ApiV1StudentGetSchema:
    """Создать нового студента (требование 1)"""
    new_student = Student(
        id=student.id,
        name=student.name,
        number=student.number
    )
    created_student = group_persistence.create_student(new_student)
    return ApiV1StudentGetSchema(
        id=created_student.id,
        name=created_student.name,
        number=created_student.number
    )


@router.delete("/students/{student_id}", summary="Delete student", response_model=ApiV1StudentDeleteResponseSchema)
async def delete_student(
        student_id: UUID,
        group_persistence: BaseGroupPersistence = Depends(group_persistence_dependency)
) -> ApiV1StudentDeleteResponseSchema:
    """Удалить студента (требование 5)"""
    if not group_persistence.get_student_by_id(student_id):
        raise HTTPException(status_code=404, detail="Student not found")

    group_persistence.delete_student(student_id)
    return ApiV1StudentDeleteResponseSchema(
        success=True,
        message="Student successfully deleted",
        student_id=student_id
    )


# Эндпоинты для управления студентами в группах
@router.get("/groups/{group_id}/students", summary="Get students in group", response_model=ApiV1GroupStudentsSchema)
async def get_group_students(
        group_id: UUID,
        group_persistence: BaseGroupPersistence = Depends(group_persistence_dependency)
) -> ApiV1GroupStudentsSchema:
    """Получить всех студентов в группе (требование 11)"""
    group = group_persistence.get_by_id(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    students = group_persistence.get_group_students(group_id)
    return ApiV1GroupStudentsSchema(
        group_id=group.id,
        group_name=group.name,
        students=[
            ApiV1StudentGetSchema(
                id=student.id,
                name=student.name,
                number=student.number
            ) for student in students
        ]
    )


@router.post("/groups/assign-student", summary="Assign student to group")
async def assign_student_to_group(
        assignment: ApiV1StudentGroupAssignSchema,
        group_persistence: BaseGroupPersistence = Depends(group_persistence_dependency)
):
    """Добавить студента в группу (требование 9)"""
    if not group_persistence.get_student_by_id(assignment.student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    if not group_persistence.get_by_id(assignment.group_id):
        raise HTTPException(status_code=404, detail="Group not found")

    group_persistence.assign_student_to_group(assignment.student_id, assignment.group_id)
    return {"message": "Student successfully assigned to group"}


@router.post("/groups/remove-student", summary="Remove student from group")
async def remove_student_from_group(
        removal: ApiV1StudentGroupRemoveSchema,
        group_persistence: BaseGroupPersistence = Depends(group_persistence_dependency)
):
    """Удалить студента из группы (требование 10)"""
    if not group_persistence.get_student_by_id(removal.student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    if not group_persistence.get_by_id(removal.group_id):
        raise HTTPException(status_code=404, detail="Group not found")

    group_persistence.remove_student_from_group(removal.student_id, removal.group_id)
    return {"message": "Student successfully removed from group"}


@router.post("/groups/transfer-student", summary="Transfer student between groups")
async def transfer_student(
        transfer: ApiV1StudentGroupTransferSchema,
        group_persistence: BaseGroupPersistence = Depends(group_persistence_dependency)
):
    """Перевести студента из одной группы в другую (требование 12)"""
    if not group_persistence.get_student_by_id(transfer.student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    if not group_persistence.get_by_id(transfer.from_group_id):
        raise HTTPException(status_code=404, detail="Source group not found")
    if not group_persistence.get_by_id(transfer.to_group_id):
        raise HTTPException(status_code=404, detail="Destination group not found")

    group_persistence.transfer_student_between_groups(
        transfer.student_id,
        transfer.from_group_id,
        transfer.to_group_id
    )
    return {"message": "Student successfully transferred between groups"}