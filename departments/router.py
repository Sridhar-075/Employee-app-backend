from fastapi import APIRouter, Depends
from auth.dependencies import get_current_user
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from departments.schemas import DepartmentCreate, DepartmentResponse
from departments import service

router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
    dependencies=[Depends(get_current_user)],
)


@router.post("/", response_model=DepartmentResponse)
async def create_department(body: DepartmentCreate, db: AsyncSession = Depends(get_db)):
    department = await service.create_department(db, body)
    return department


@router.get("/", response_model=list[DepartmentResponse])
async def get_all_departments(db: AsyncSession = Depends(get_db)):
    departments = await service.get_employees_service(db)
    return departments


@router.post("/{id}")
async def update_department(
    body: DepartmentCreate, id: int, db: AsyncSession = Depends(get_db)
):
    await service.update_employee_service(db, id, body)
    return "updated department"
