from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.s_payslip import PayslipResponse,PayslipCreate
from app.crud import c_payslip

router = APIRouter(prefix="/payslip", tags=["payslip"])

@router.post('/', response_model=PayslipResponse, status_code=201)
def generate_payslip(payload: PayslipCreate,  db: Session = Depends(get_db.getDB)):
    return c_payslip.generate_emp_payslip(db, payload.employee_id, start=payload.period_start,
        end=payload.period_end,
        payout=payload.payout_date)

@router.get('/{payslip_id}', response_model=PayslipResponse, status_code=200)
def get_payslip(payslip_id: int, db: Session = Depends(get_db.getDB)):
    return c_payslip.get_payslip(db, payslip_id)

@router.get('/employee/{employee_id}', response_model=list[PayslipResponse], status_code=200)
def get_employee_payslips(employee_id: int, db: Session = Depends(get_db.getDB)):
    return c_payslip.get_employee_payslips(db, employee_id)

@router.get('/', response_model=list[PayslipResponse], status_code=200)
def get_all_payslips(db: Session = Depends(get_db.getDB)):
    return c_payslip.get_all_payslips(db)  

@router.delete('/{payslip_id}', response_model=PayslipResponse, status_code=200)
def delete_payslip(payslip_id: int, db: Session = Depends(get_db.getDB)):
    return c_payslip.delete_payslip(db, payslip_id)