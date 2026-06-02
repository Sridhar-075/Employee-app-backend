from exceptions import UnauthorizedException
from auth.utils import verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from employees import repo

from auth.utils import create_access_token, create_refresh_token, decode_refresh_token


async def login(db: AsyncSession, email: str, password: str):
    employee = await repo.get_by_email(db, email)
    if employee is None:
        raise UnauthorizedException("Invalid email or password")
    if not verify_password(password, employee.password_hash):
        raise UnauthorizedException("Invalid email or password")
    payload = {"id": employee.id, "email": employee.email, "role": employee.role.value}

    return {
        "access_token": create_access_token(payload),
        "refresh_token": create_refresh_token(payload),
        "token_type": "bearer",
    }


async def refresh(refresh_token: str):
    payload = decode_refresh_token(refresh_token)

    if payload is None:
        raise UnauthorizedException("Invalid refresh token")

    if payload.get("type") != "refresh":
        raise UnauthorizedException("Invalid refresh token")

    new_payload = {
        "id": payload["id"],
        "email": payload["email"],
        "role": payload["role"],
    }

    return {"access_token": create_access_token(new_payload), "token_type": "bearer"}
