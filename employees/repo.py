"""Employee Repo"""

from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from models.employee import Employee
from models.address import Address
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from models.department import Departments
from exceptions import ConflictException, NotFoundException


async def get_all_employees(db: AsyncSession):
    stmt = (
        select(Employee)
        .options(selectinload(Employee.addresses))
        .where(Employee.deleted_at.is_(None))
    )
    result = await db.scalars(stmt)
    return result


async def get_by_email(db: AsyncSession, email: str) -> Employee | None:
    stmt = select(Employee).where(
        Employee.email == email, Employee.deleted_at.is_(None)
    )
    employee = await db.scalars(stmt)

    return employee.first()


async def create(
    db: AsyncSession,
    name: str,
    email: str,
    password: str,
    age: int,
    line1: str,
    city: str,
    postalcode: int,
    country: str,
    role: str,
) -> Employee:
    db_employee = Employee(
        name=name,
        email=email,
        password_hash=password,
        age=age,
        role=role,
        addresses=[
            Address(
                line1=line1,
                city=city,
                postalcode=postalcode,
                country=country,
            )
        ],
    )
    db.add(db_employee)

    try:
        await db.commit()
        await db.refresh(db_employee)
        stmt = (
            select(Employee)
            .options(selectinload(Employee.addresses))
            .where(Employee.id == db_employee.id)
        )
        result = await db.execute(stmt)
        return result.scalar_one()
    except IntegrityError:
        await db.rollback()
        raise ConflictException(f"Email '{email.strip()} is already in use")


async def search_by_name(name: str, db: AsyncSession):
    stmt = (
        select(Employee)
        .options(selectinload(Employee.addresses))
        .where(Employee.deleted_at is None)
        .where(Employee.name == name)
    )
    result = await db.scalars(stmt)
    employees = result.all()
    return employees


async def get_by_id(db: AsyncSession, id: int):
    stmt = (
        select(Employee)
        .options(selectinload(Employee.addresses))
        .where(Employee.id == id)
    )
    result = await db.scalars(stmt)

    # res = [r.to_api_dict() for r in result.all()]
    return result.first()


async def delete_by_id(db: AsyncSession, id: int):
    stmt = update(Employee).where(Employee.id == id).values(deleted_at=datetime.now())
    await db.execute(stmt)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
    return


async def employee_id_add_address(
    db: AsyncSession, id: int, line1: str, city: str, postalcode: str, country: str
):
    stmt = (
        select(Employee)
        .options(selectinload(Employee.addresses))
        .where(Employee.id == id)
    )
    result = await db.execute(stmt)
    employee = result.scalar_one()
    employee.addresses.append(
        Address(line1=line1, city=city, postalcode=postalcode, country=country)
    )
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()

    return


async def employee_add_department(id: int, department_id: int, db: AsyncSession):
    stmt = (
        select(Employee)
        .options(selectinload(Employee.departments))
        .where(Employee.id == id)
    )
    result = await db.execute(stmt)
    employee = result.scalar_one()
    stmt2 = select(Departments).where(Departments.id == department_id)
    result2 = await db.execute(stmt2)
    department = result2.scalar_one()
    employee.departments.append(department)
    try:
        await db.commit()
        return
    except IntegrityError:
        await db.rollback()

    return


async def employee_update(id, db: AsyncSession, body):
    stmt = update(Employee).where(Employee.id == id).values(**body)
    await db.execute(stmt)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
    return


async def detatch_department(id, department_id, db: AsyncSession):
    stmt = (
        select(Employee)
        .options(selectinload(Employee.departments))
        .where(Employee.id == id)
    )
    result = await db.execute(stmt)
    employee = result.scalar_one()
    stmt2 = select(Departments).where(Departments.id == department_id)
    result2 = await db.execute(stmt2)
    department = result2.scalar_one()
    employee.departments.remove(department)
    try:
        await db.commit()
        return
    except IntegrityError:
        await db.rollback()

    return


async def delete_address(id, address_id, db: AsyncSession):
    stmt = select(Address).where(Address.id == address_id)
    result = await db.scalars(stmt)
    address = result.first()
    if address.employee_id != id:
        raise NotFoundException("No Employee exists with matching address")

    stmt2 = (
        update(Address)
        .where(Address.id == address_id)
        .values(deleted_at=datetime.now())
    )
    await db.execute(stmt2)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
