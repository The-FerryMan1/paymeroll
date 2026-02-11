from datetime import date, time
from typing import TYPE_CHECKING

from sqlalchemy import Date, Float, ForeignKey, Integer, String, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.employee import Employee


class Attendance(Base):
    __tablename__ = "attendance"

    id: Mapped[int] = mapped_column(index=True, primary_key=True)
    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))

    work_date: Mapped[date] = mapped_column(Date, index=True)

    time_in: Mapped[time | None] = mapped_column(Time)
    time_out: Mapped[time | None] = mapped_column(Time)

    minutes_late: Mapped[int] = mapped_column(Integer, default=0)
    minutes_undertime: Mapped[int] = mapped_column(Integer, default=0)
    overtime_hours: Mapped[float] = mapped_column(Float, default=0.0)

    status: Mapped[str] = mapped_column(String(20), default="PRESENT")

    employee: Mapped["Employee"] = relationship()

    __table_args__ = (
        UniqueConstraint("employee_id", "work_date", name="uq_employee_date"),
    )
