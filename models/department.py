from models.entity import Entity
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from models.employee_department import employee_department


class Departments(Entity):
    __tablename__ = "departments"
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    employees = relationship(
        "Employee", secondary=employee_department, back_populates="departments"
    )
