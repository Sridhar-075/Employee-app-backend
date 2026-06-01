from datetime import datetime
from pydantic import BaseModel


class DepartmentCreate(BaseModel):
    name: str


class DepartmentResponse(DepartmentCreate):
    id: int
    created_at: datetime
    updated_at: datetime
