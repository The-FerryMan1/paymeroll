from typing import Annotated, List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.crud import c_employee
from app.dependencies import get_db
from app.schemas.s_employee import CreateEmployee, Employee, UpdateEmployee

router = APIRouter(prefix="/employee", tags=["employee"])


@router.get("/", response_model=List[Employee])
async def get_all_employees(
    skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db.getDB)
):
    return await c_employee.get_all_employee(db, skip=skip, limit=limit)


@router.get("/{employee_id}", response_model=Employee, status_code=HTTP_200_OK)
async def get_employee(
    employee_id: Annotated[int, Path(title="employee ID")],
    db: AsyncSession = Depends(get_db.getDB),
):
    return await c_employee.get_employee(db, employee_id)


@router.post("/", response_model=Employee, status_code=HTTP_201_CREATED)
async def create_employee(
    employee: CreateEmployee, db: AsyncSession = Depends(get_db.getDB)
):
    return await c_employee.create_employee(db, employee)


@router.put("/{employee_id}", response_model=Employee, status_code=HTTP_200_OK)
async def update_employee(
    employee_id: Annotated[int, Path(title="Employee ID")],
    employee: UpdateEmployee,
    db: AsyncSession = Depends(get_db.getDB),
):
    return await c_employee.update_employee(db, employee_id, employee)


@router.delete("/{employee_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_employee(
    employee_id: Annotated[int, Path(title="Employee ID")],
    db: Annotated[AsyncSession, Depends(get_db.getDB)],
):
    return await c_employee.delete_employee(db, employee_id)
