"""Employee Service"""

import employees.repo as repo
from sqlalchemy.ext.asyncio import AsyncSession
from exceptions import NotFoundException, BadRequestException
from models.employee import Employee
from auth.utils import hash_password


async def get_all_employees(db: AsyncSession):
    employees = await repo.get_all_employees(db)
    return employees


async def create(db: AsyncSession, body) -> Employee:
    if not isinstance(body.name, str) or not body.name.strip():
        raise BadRequestException("name must be a non-empty string")
    if not isinstance(body.email, str) or not body.email.strip():
        raise BadRequestException("email must be a non-empty string")
    hashed = hash_password(body.password)
    employee = await repo.create(
        db,
        name=body.name.strip(),
        email=body.email.strip(),
        password=hashed,
        age=body.age,
        line1=body.address.line1,
        city=body.address.city,
        postalcode=body.address.postalcode,
        country=body.address.country,
        role=body.role,
    )

    return employee


async def search_by_name_service(name: str, db: AsyncSession):
    employees = await repo.search_by_name(name, db)
    return [e.to_api_dict() for e in employees]


async def get_by_id(db: AsyncSession, id: int):
    employee = await repo.get_by_id(db, id)
    if employee is None:
        raise NotFoundException(f"Employee with id: {id} not found")
    return employee


async def delete_by_id(db: AsyncSession, id: int):
    await repo.delete_by_id(db, id)
    return


async def add_address(db: AsyncSession, id, body):
    await repo.employee_id_add_address(
        db, id, body.line1, body.city, body.postalcode, body.country
    )
    return


async def employee_add_department(db: AsyncSession, id: int, department_id: int):
    await repo.employee_add_department(id, department_id, db)
    return


async def update_employee_service(id, db: AsyncSession, body):
    updates = body.model_dump(exclude_unset=True)
    await repo.employee_update(id, db, updates)
    return
