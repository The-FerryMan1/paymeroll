from fastapi import HTTPException
from sqlalchemy import and_, or_, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from app.models.employee import Employee
from app.schemas.s_employee import CreateEmployee, UpdateEmployee


async def get_all_employee(db: AsyncSession, skip: int = 0, limit: int = 50):
    result =  await db.execute(select(Employee).offset(skip).limit(limit))
    return result.scalars().all()


async def get_employee(db: AsyncSession, employee_id: int):
    stmt = await db.execute(
        select(Employee).where(Employee.id == employee_id)
    )

    emp = stmt.scalar_one_or_none()
    if not emp:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Employee with the ID of {employee_id} does not exists.",
        )
    return stmt.scalar_one_or_none()


async def create_employee(db: AsyncSession, employee: CreateEmployee):

    check = await db.execute(
        select(Employee).where(
            or_(
                Employee.tin_no == employee.tin_no,
                Employee.sss_no == employee.sss_no,
                Employee.philhealth_no == employee.philhealth_no,
                Employee.pagibig_no == employee.pagibig_no,
            )
        )
    )

    existing_no = check.scalar_one_or_none()
    if existing_no:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"""These numbers are already taken: [{"tin" if existing_no.tin_no else ""},{"sss" if existing_no.sss_no else ""},{"philhealth" if existing_no.philhealth_no else ""},{"pagibig" if existing_no.pagibig_no else ""}]""",
        )

    stmt = Employee(**employee.model_dump())
    db.add(stmt)
    await db.commit()
    await db.refresh(stmt)
    return stmt


async def update_employee(db: AsyncSession, employee_id: int, employee_data: UpdateEmployee):
    update_data =  employee_data.model_dump(exclude_unset=True)

    check = await db.execute(
        select(Employee).where(
            and_(
                Employee.id != employee_id,
                or_(
                    Employee.tin_no == update_data.get("tin_no"),
                    Employee.sss_no == update_data.get("sss_no"),
                    Employee.pagibig_no == update_data.get("pagibig_no"),
                    Employee.philhealth_no == update_data.get("philhealth_no"),
                ),
            )
        )
    )

    conflict = check.scalar_one_or_none()

    if conflict:
        raise HTTPException(
            status_code=400,
            detail="Update Failed: One of the government IDs is already assigned to another employee.",
        )

    if update_data:
        await db.execute(
            update(Employee).where(Employee.id == employee_id).values(**update_data)
        )
        await db.commit()
    return  await get_employee(db, employee_id)


async def delete_employee(db: AsyncSession, employee_id: int):
    employee = await get_employee(db, employee_id)

    if not employee:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Employee with the ID of {employee_id} does not exists.",
        )
    await db.delete(employee)
    await db.commit()
    return True
