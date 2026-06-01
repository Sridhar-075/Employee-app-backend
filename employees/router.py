"""Employee Router"""

from fastapi import APIRouter, Depends, status
from database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from employees import service, schemas
from auth.dependencies import get_current_user, require_role
from models.employee import EmployeeRole


router = APIRouter(
    prefix="/employees",
    tags=["Employees"],
)


@router.get(
    "/",
    tags=["Employees"],
    response_model=list[schemas.EmployeeResponse],
    dependencies=[Depends(get_current_user)],
)
async def get_all_employees(db: AsyncSession = Depends(get_db)):
    response = await service.get_all_employees(db)
    return response


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.EmployeeResponse,
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def create_employee(
    body: schemas.EmployeeCreate, db: AsyncSession = Depends(get_db)
):
    # name = body.get("name")
    # email = body.get("email")

    employee = await service.create(db, body)
    return employee


# @router.delete("/{id}")
# async def delete_employee(id:int,db: AsyncSession = Depends(get_db)):


@router.get("/search", response_model=list[schemas.EmployeeResponseId])
async def search_by_name(name: str, db: AsyncSession = Depends(get_db)):
    employees = await service.search_by_name_service(name, db)
    return employees


@router.post(
    "/update/{id}",
    status_code=status.HTTP_200_OK,
    tags=["Employees"],
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def update_employee(
    id: int, body: schemas.EmployeeUpdate, db: AsyncSession = Depends(get_db)
):
    await service.update_employee_service(id, db, body)
    return "Employee updated"


@router.post(
    "/employee/{id}/address", dependencies=[Depends(require_role(EmployeeRole.HR))]
)
async def employee_add_address(
    id: int, body: schemas.AddressCreate, db: AsyncSession = Depends(get_db)
):
    employee = await service.add_address(db, id, body)
    return "Address added"


@router.post(
    "/employee/{id}/department/{department_id}",
    dependencies=[Depends(require_role(EmployeeRole.HR))],
)
async def add_department(
    id: int, department_id: int, db: AsyncSession = Depends(get_db)
):
    await service.employee_add_department(db, id, department_id)
    return "Department added"


@router.get("/{id}", response_model=schemas.EmployeeResponseId)
async def get_by_id(
    id: int,
    db: AsyncSession = Depends(get_db),
    # _current_user:TokenPayload = Depends(get_current_user)
):
    employee = await service.get_by_id(db, id)
    return employee


@router.delete("/{id}", dependencies=[Depends(require_role(EmployeeRole.HR))])
async def delete_by_id(id: int, db: AsyncSession = Depends(get_db)):
    await service.delete_by_id(db, id)
    return "Employee Deleted"
