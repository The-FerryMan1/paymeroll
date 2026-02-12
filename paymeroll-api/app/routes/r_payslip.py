from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.s_payslip import PayslipResponse,PayslipCreate
from app.crud import c_payslip

router = APIRouter(prefix="/payslip", tags=["payslip"])

@router.post('/', response_model=PayslipResponse)
def generate_payslip(payload: PayslipCreate,  db: Session = Depends(get_db.getDB)):
    return c_payslip.generate_emp_payslip(db, payload.employee_id, start=payload.period_start,
        end=payload.period_end,
        payout=payload.payout_date)