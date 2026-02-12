from fastapi import Depends, FastAPI
from sqlalchemy.orm.session import Session

from app.core.database import Base, engine
from app.dependencies.get_db import getDB
from app.models.attendance import Attendance
from app.models.employee import Employee
from app.models.payslip import Payslip
from app.models.user import User
from app.routes import r_attendance, r_employee, r_payslip

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Paymeroll API")

app.include_router(r_employee.router)
app.include_router(r_attendance.router)
app.include_router(r_payslip.router)


@app.get("/")
async def root():
    return "Paymeroll API is running!"


@app.get("/db_check")
async def db_check(db: Session = Depends(getDB)):
    return {"connection": "up"}
