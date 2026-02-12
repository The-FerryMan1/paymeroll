from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict

class EmployeeBase(BaseModel):
    full_name: str
    tin_no: str
    sss_no: str
    philhealth_no: str
    pagibig_no: str
    pay_basis: str
    pay_frequency: str
    base_rate: float
    de_minimis_allowance: float
    is_active: bool
    hire_date: date


class CreateEmployee(EmployeeBase):
    pass


class UpdateEmployee(BaseModel):
    full_name: Optional[str] = None
    tin_no: Optional[str] = None
    sss_no: Optional[str] = None
    philhealth_no: Optional[str] = None
    pagibig_no: Optional[str] = None
    pay_basis: Optional[str] = None
    pay_frequency: Optional[str] = None
    base_rate: Optional[float] = None
    de_minimis_allowance: Optional[float] = None
    is_active: Optional[bool] = None


class Employee(EmployeeBase):
    id: int
    employee_no: str
    model_config = ConfigDict(from_attributes=True)
