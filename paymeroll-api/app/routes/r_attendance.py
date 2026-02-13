from typing import Annotated, List

from fastapi import Depends, Path, Query
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.crud import c_attendance
from app.dependencies import get_db
from app.schemas.s_attendance import (
    AttendanceCreate,
    AttendanceResponse,
    AttendanceUpdate,
)

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post("/", response_model=AttendanceResponse, status_code=HTTP_201_CREATED)
async def create_attendance(
    attendance: AttendanceCreate, db: AsyncSession = Depends(get_db.getDB)
):
    return c_attendance.create_attendance(db, attendance)


@router.get("/", response_model=List[AttendanceResponse], status_code=HTTP_200_OK)
async def get_all_attendances(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db.getDB),
):
    return await c_attendance.get_all_attendance(db, skip, limit)


@router.get(
    "/{attendance_id}",
    response_model=AttendanceResponse,
    status_code=HTTP_200_OK,
)
async def get_attendance(
    attendance_id: Annotated[int, Path(title="Attendance ID")],
    db: AsyncSession = Depends(get_db.getDB),
):
    return await c_attendance.get_attendance(db, attendance_id)


@router.get(
    "/employee/{employee_id}",
    response_model=List[AttendanceResponse],
    status_code=HTTP_200_OK,
)
async def get_emp_attendance(
    employee_id: Annotated[int, Path(title="Employee ID")],
    db: AsyncSession = Depends(get_db.getDB),
):
    return await c_attendance.get_emp_attendances(db, employee_id)


@router.put(
    "/{attendance_id}", response_model=AttendanceResponse, status_code=HTTP_200_OK
)
async def update_attendance(
    attendance_id: Annotated[int, Path(title="Attendance ID")],
    time_out: AttendanceUpdate,
    db: AsyncSession = Depends(get_db.getDB),
):
    return await c_attendance.update_clock_out(db, attendance_id, time_out.time_out)


@router.delete("/{attendance_id}", status_code=HTTP_204_NO_CONTENT)
async def delete_attendance(
    attendance_id: Annotated[int, Path(title="Attendance ID")],
    db: AsyncSession = Depends(get_db.getDB),
):
    return await c_attendance.delete_attendance(db, attendance_id)
