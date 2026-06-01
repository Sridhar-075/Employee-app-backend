from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from models.department import Departments
from sqlalchemy.exc import IntegrityError

async def create_department(db:AsyncSession,name:str):
    db_department = Departments(
        name=name
    )
    db.add(db_department)
    try:
        await db.commit()
        await db.refresh(db_department)
        print("db")
        print(db_department)
        return db_department
    except IntegrityError:
        await db.rollback()
    

async def get_departments(db:AsyncSession):
    stmt=select(Departments).where(Departments.deleted_at.is_(None))
    result = await db.scalars(stmt)
    return result

async def update_department_by_id(db:AsyncSession,id:int,name:str):
    stmt = update(Departments).where(Departments.id==id).values(name=name)
    await db.execute(stmt)
    try:
        await db.commit()
        return
    except IntegrityError:
        await db.rollback
        return
    