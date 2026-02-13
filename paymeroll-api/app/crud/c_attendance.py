from datetime import time
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException
from sqlalchemy import and_, select, update
from sqlalchemy.orm import Session
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from app.crud.c_employee import get_employee
from app.models.attendance import Attendance
from app.models.employee import Employee
from app.schemas.s_attendance import AttendanceCreate, AttendanceUpdate


def calc_attendance_metric(time_in: time | None, time_out: time | None):

    if not time_in or not time_out:
        return 0, 0, 0.0

    start_shift = time(8, 0, 0, 0)
    end_shift = time(17, 0, 0, 0)

    def to_mins(t: time):
        return t.hour * 60 + t.minute

    ut = 0
    ot = 0
    late: float = 0.0

    if time_in > start_shift:
        late = to_mins(time_in) - to_mins(start_shift)
    if time_out < end_shift:
        ut = to_mins(time_out) - to_mins(end_shift)
    if time_out > end_shift:
        ot_mins = to_mins(time_out) - to_mins(end_shift)
        ot = round(ot_mins / 60, 2)
    return late, ut, ot


async def create_attendance(db: AsyncSession, attendance_in: AttendanceCreate):

    employee = get_employee(db, attendance_in.employee_id)

    if not employee:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Employee with an ID of {attendance_in.employee_id} does not exists",
        )
    existing_record = await db.execute(
        select(Attendance).where(
            Attendance.employee_id == attendance_in.employee_id,
            Attendance.work_date == attendance_in.work_date,
        )
    )
    existing_record = existing_record.scalar_one_or_none()

    if existing_record:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Employee {attendance_in.employee_id} already has a record for {attendance_in.work_date}.",
        )

    late, ut, ot = calc_attendance_metric(attendance_in.time_in, attendance_in.time_out)

    db_attendance = Attendance(
        **attendance_in.model_dump(),
        minutes_late=int(late),
        minutes_undertime=ut,
        overtime_hours=ot,
    )

    db.add(db_attendance)
    await db.commit()
    await db.refresh(db_attendance)
    return db_attendance


async def get_all_attendance(db: AsyncSession, skip: int, limit: int):
    stmt = await db.execute(select(Attendance).offset(skip).limit(limit))
    return stmt.scalars().all()


async def get_attendance(db: AsyncSession, attendance_id: int):
    stmt = await db.execute(
        select(Attendance).where(Attendance.id == attendance_id)
    )
    stmt = stmt.scalar_one_or_none()
    if not stmt:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Attendance with an ID of {attendance_id} does not exists",
        )

    return stmt


async def get_emp_attendances(db: AsyncSession, employee_id: int):

    employee = await get_employee(db, employee_id)

    if not employee:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Employee with an ID of {employee_id} does not exists",
        )

    stmt = await (
        db.execute(select(Attendance).where(Attendance.employee_id == employee_id))
    )
    stmt = stmt.scalars().all()
    return stmt


async def update_clock_out(db: AsyncSession, attendance_id: int, time_out: time):

    db_attendance = await db.execute(select(Attendance).where(Attendance.id == attendance_id))
    db_attendance = db_attendance.scalar_one_or_none()
    print(db_attendance)

    if db_attendance:
        db_attendance.time_out = time_out

        late, ut, ot = calc_attendance_metric(db_attendance.time_in, time_out)

        db_attendance.minutes_late = int(late)
        db_attendance.minutes_undertime = ut
        db_attendance.overtime_hours = ot

        await db.commit()
        await db.refresh(db_attendance)
    return db_attendance


async def delete_attendance(db: AsyncSession, attendance_id: int):
    attendance = await get_attendance(db, attendance_id)

    if not attendance:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Attendance with an ID of {attendance_id} does not exists",
        )
    await db.delete(attendance)
    await db.commit()
    return True
