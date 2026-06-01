from sqlalchemy import ForeignKey, Column, Table
from database import Base

employee_department = Table(
    "employee_department",
    Base.metadata,
    Column("employee_id", ForeignKey("employees.id"), primary_key=True),
    Column("department_id", ForeignKey("departments.id"), primary_key=True),
)
