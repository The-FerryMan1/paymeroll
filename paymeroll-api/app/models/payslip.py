from datetime import date, datetime
from typing import TYPE_CHECKING
from uuid import uuid8

from sqlalchemy import Date, DateTime, Float, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.employee import Employee
    from app.models.user import User


class Payslip(Base):
    __tablename__ = "payslip"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    payslip_no: Mapped[str] = mapped_column(
        unique=True, index=True, default=lambda: str(uuid8())
    )
    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
    created_by_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    # timing
    payout_date: Mapped[date] = mapped_column(Date)
    period_start: Mapped[date] = mapped_column(Date)
    period_end: Mapped[date] = mapped_column(Date)

    # Totals
    gross_pay: Mapped[float] = mapped_column(Float)
    net_pay: Mapped[float] = mapped_column(Float)

    # 2026 Employee Deductions
    sss_ee: Mapped[float] = mapped_column(Float)  # 5% Share
    philhealth_ee: Mapped[float] = mapped_column(Float)  # 2.5% Share
    pagibig_ee: Mapped[float] = mapped_column(Float)  # Max 200
    withholding_tax: Mapped[float] = mapped_column(Float)

    # 2026 Employer Contributions (For your Gov Reports)
    sss_er: Mapped[float] = mapped_column(Float)  # 10% Share
    philhealth_er: Mapped[float] = mapped_column(Float)  # 2.5% Share
    pagibig_er: Mapped[float] = mapped_column(Float)  # Max 200

    # employee relation
    employee: Mapped["Employee"] = relationship(back_populates="payslips")

    # User relation(admin)
    creator: Mapped["User"] = relationship()

    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
