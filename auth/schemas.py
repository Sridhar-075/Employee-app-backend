from pydantic import BaseModel
from models.employee import EmployeeRole


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenPayload(BaseModel):
    """Decoded JWT payload."""

    id: int
    email: str
    role: EmployeeRole


class RefreshTokenRequest(BaseModel):
    refresh_token: str
