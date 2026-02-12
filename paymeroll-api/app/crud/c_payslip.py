
from datetime import date
from sqlalchemy.orm import Session
from app.models.payslip import Payslip
from app.services.v_payslip import calculate_deductions
from app.models.employee import Employee


# creator_id: int,
def generate_emp_payslip(db: Session, employee_id: int,  start: date, end: date, payout: date):
    emp = db.get(Employee, employee_id)
    if not emp: return None

    (gross_pay, sss_ee, sss_er, 
    ph_ee, ph_er, pagibig_ee, 
    pagibig_er, taxable, tax, net_pay) = calculate_deductions(emp.base_rate)

    new_payslip = Payslip(
        employee_id=employee_id,
        created_by_id=1,
        payout_date=payout,
        period_start=start,
        period_end=end,
        gross_pay=round(gross_pay, 2),
        net_pay=round(net_pay, 2),
        sss_ee=round(sss_ee, 2),
        sss_er=round(sss_er, 2),
        philhealth_ee=round(ph_ee, 2),
        philhealth_er=round(ph_er, 2),
        pagibig_ee=round(pagibig_ee, 2),
        pagibig_er=round(pagibig_er, 2),
        withholding_tax=round(tax, 2)
    )

    db.add(new_payslip)
    db.commit()
    db.refresh(new_payslip)
    return new_payslip

    
    