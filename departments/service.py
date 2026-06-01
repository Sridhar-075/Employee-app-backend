from sqlalchemy.ext.asyncio import AsyncSession
from departments import repo


async def create_department(db: AsyncSession, body):
    department = await repo.create_department(db, body.name)
    return department


async def get_employees_service(db: AsyncSession):
    departments = await repo.get_departments(db)
    return departments


async def update_employee_service(db: AsyncSession, id: int, body):
    await repo.update_department_by_id(db, id, body.name)
    return
