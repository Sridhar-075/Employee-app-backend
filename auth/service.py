from exceptions import UnauthorizedException
from auth.utils import verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from employees import repo
from auth.utils import create_access_token


async def login(db:AsyncSession,email:str, password:str) ->str:
    employee = await repo.get_by_email(db,email)
    if employee is None:
        raise UnauthorizedException("Invalid email or passowrd")
    
    if not verify_password(password, employee.password_hash):
        raise UnauthorizedException("Invalid email or passowrd")
    
    return create_access_token({"id":employee.id, "email":employee.email,"role":employee.role.value})