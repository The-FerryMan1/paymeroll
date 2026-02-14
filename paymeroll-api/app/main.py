from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import Base, engine
from app.dependencies.get_db import getDB
from app.models.employee import Employee
from app.models.attendance import Attendance
from app.models.payslip import Payslip
from app.models.user import User
from app.routes import r_attendance, r_employee, r_payslip, r_auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

    await engine.dispose()

app = FastAPI(title="Paymeroll API", lifespan=lifespan )

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(r_employee.router)
app.include_router(r_attendance.router)
app.include_router(r_payslip.router)
app.include_router(r_auth.router)


@app.get("/")
async def root():
    return "Paymeroll API is running!"


@app.get("/db_check")
async def db_check(db: AsyncSession = Depends(getDB)):
    return {"connection": "up"}
