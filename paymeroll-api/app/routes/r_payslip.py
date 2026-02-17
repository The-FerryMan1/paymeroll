from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.types import ASGIApp

from app.core.auth import CurrentUser, admin_check
from app.crud import c_payslip
from app.dependencies import get_db
from app.schemas.s_payslip import PayslipCreate, PayslipResponse

router = APIRouter(prefix="/payslip", tags=["payslip"])


@router.post(
    "/",
    response_model=PayslipResponse,
    status_code=201,
    dependencies=[Depends(admin_check)],
)
async def generate_payslip(
    payload: PayslipCreate,
    created_by: CurrentUser,
    db: AsyncSession = Depends(get_db.getDB),
):
    return await c_payslip.generate_emp_payslip(
        db,
        payload.employee_id,
        created_by_id=created_by.id,
        start=payload.period_start,
        end=payload.period_end,
        payout=payload.payout_date,
    )


@router.get(
    "/{payslip_id}",
    response_model=PayslipResponse,
    status_code=200,
)
async def get_payslip(payslip_id: int, db: AsyncSession = Depends(get_db.getDB)):
    return await c_payslip.get_payslip(db, payslip_id)


@router.get(
    "/employee/{employee_id}", response_model=list[PayslipResponse], status_code=200
)
async def get_employee_payslips(
    employee_id: int, db: AsyncSession = Depends(get_db.getDB)
):
    return await c_payslip.get_employee_payslips(db, employee_id)


@router.get("/", response_model=list[PayslipResponse], status_code=200)
async def get_all_payslips(db: AsyncSession = Depends(get_db.getDB)):
    return await c_payslip.get_all_payslips(db)


@router.delete(
    "/{payslip_id}",
    response_model=PayslipResponse,
    status_code=200,
    dependencies=[Depends(admin_check)],
)
async def delete_payslip(payslip_id: int, db: AsyncSession = Depends(get_db.getDB)):
    return await c_payslip.delete_payslip(db, payslip_id)


@router.get("/{payslip_id}/csv")
async def generate_payslip_csv(
    payslip_id: int, db: Annotated[AsyncSession, Depends(get_db.getDB)]
):
    return await c_payslip.generate_csv_payslip(db, payslip_id)
