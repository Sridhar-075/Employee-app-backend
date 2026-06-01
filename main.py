import logging
from fastapi import FastAPI
from employees import employee_router
from middleware import configure_middleware
from config import settings
from exceptions.handlers import register_exception_handler
from auth.router import router as auth_router
from departments import router as department_router

# from database import create_tables
_employees: dict[int, dict] = {}
_next_id: int = 1

# @dataclass
# class CreateEmployee:
#     first_name:str
#     last_name:str

# class CreateEmployeeResponse(TypedDict):
#     id:int
#     first_name:str
#     last_name:str


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     await create_tables()
#     yield


app = FastAPI(
    title="Employee CRUD API",
    description="Was a Simple API with dict storage, now with DBMS",
    version="1.0.0",
    # lifespan=lifespan
)

app.include_router(auth_router)
configure_middleware(app)
register_exception_handler(app)
app.include_router(department_router)
app.include_router(employee_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "env": settings.app_env, "debug": settings.debug}


@app.get("/")
def root():
    return "Welcome to Employee CRUD API"


# ---------------------

# @app.get("/employee")
# def get_employee():
#     return _employees

# ---------------------

# @app.get("/employee", tags=["Employees"],response_model=list[EmployeeResponse])
# async def get_all_employees(db: AsyncSession = Depends(get_db)):
#     stmt = select(Employee).where(Employee.deleted_at.is_(None))
#     result = await db.scalars(stmt)
#     res = [r.to_api_dict() for r in result.all()]
#     print(result)
#     print(res)
#     return res

# @app.delete("/employee/{id}")
# async def delete(id:int, db: AsyncSession = Depends(get_db)):
#     stmt = update(Employee).where(Employee.id==id).values(deleted_at=datetime.now())
#     result = await db.execute(stmt)
#     await db.commit()
#     # res = [r.to_api_dict() for r in result.all()]

#     return result


# -------------------------
# @app.delete("/employee/{id}",status_code = status.HTTP_204_NO_CONTENT )
# def delete(id:int):
#     employee = _employees.get(id)
#     if (not employee or employee["isdeleted"]):
#         raise HTTPException(status_code=404,details="not found")
#     else:
#         employee[id]["isdeleted"] = True


# @app.post("/employees",
#           status_code = 201,

#           )
# def create_post(post:dict = Body(...)) -> dict:
#     global _next_id
#     global _employees
#     id = _next_id
#     _employees[id]={
#         "id": _next_id,
#         "firstname": post.get("first_name"),
#         "lastname": post.get("last_name"),
#         "isdeleted": False
#     }
#     _next_id+=1
#     return _employees[id]
# --------------------------------------

# DBMS
# @app.post("/employee", status_code=status.HTTP_201_CREATED, tags=["Employees"])
# async def create_employee(body: dict = Body(...), db: AsyncSession = Depends(get_db)):
#     name = body.get("name")
#     email = body.get("email")
#     if not isinstance(name, str) or not name.strip():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="name must be a non-empty string")
#     if not isinstance(email, str) or not email.strip():
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email must be a non-empty string")
#     db_employee = Employee(name=name.strip(), email=email.strip())
#     db.add(db_employee)
#     try:
#         await db.commit()
#     except IntegrityError:
#         await db.rollback()
#         raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email '{email.strip()}' is already in use")
#     await db.refresh(db_employee)
#     return db_employee.to_api_dict()
