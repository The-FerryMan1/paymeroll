from datetime import date
from typing import TYPE_CHECKING, List, Optional
from uuid import uuid8

from sqlalchemy import Boolean, Date, Float, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.payslip import Payslip

if TYPE_CHECKING:
    from app.models.attendance import Attendance


class Employee(Base):
    __tablename__ = "employee"

    id: Mapped[int] = mapped_column(index=True, primary_key=True)
    employee_no: Mapped[str] = mapped_column(
        String(36), default=lambda: str(uuid8()), unique=True, index=True
    )

    full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    tin_no: Mapped[Optional[str]] = mapped_column(String(20), unique=True)
    sss_no: Mapped[Optional[str]] = mapped_column(String(20), unique=True)
    philhealth_no: Mapped[Optional[str]] = mapped_column(String(20), unique=True)
    pagibig_no: Mapped[Optional[str]] = mapped_column(String(20), unique=True)

    pay_basis: Mapped[str] = mapped_column(String(20), default="MONTHLY")
    pay_frequency: Mapped[str] = mapped_column(String(20), default="SEMI_MONTHLY")
    base_rate: Mapped[float] = mapped_column(Float)

    de_minimis_allowance: Mapped[float] = mapped_column(Float, default=0.0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    hire_date: Mapped[date] = mapped_column(Date, default=func.now())

    payslips: Mapped[List["Payslip"]] = relationship(back_populates="employee")

    attendance_logs: Mapped[list["Attendance"]] = relationship(
        back_populates="employee"
    )
