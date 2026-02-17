from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class PayslipBase(BaseModel):
    employee_id: int
    payout_date: date
    period_start: date
    period_end: date


class PayslipCreate(PayslipBase):
    pass
    # created_by_id: int


class PayslipResponse(PayslipBase):
    id: int
    payslip_no: str
    gross_pay: float
    net_pay: float
    sss_ee: float
    philhealth_ee: float
    pagibig_ee: float
    withholding_tax: float
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
