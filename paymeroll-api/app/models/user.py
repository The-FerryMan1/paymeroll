import enum
from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.payslip import Payslip


class UserRole(str, enum.Enum):
    VIEWER = "VIEWER"
    ADMIN = "ADMIN"


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(255), index=True, unique=True)
    full_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    contact_no: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[str] = mapped_column(default="ADMIN")
    is_active: Mapped[bool] = mapped_column(default=True)


    processed_payslips: Mapped[List["Payslip"]] = relationship(back_populates="creator")
