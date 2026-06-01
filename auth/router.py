from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession 
from auth import service as auth_service
from auth.schemas import LoginRequest, TokenResponse
from database import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth",tags=["Auth"])

# @router.post("/login", response_model = TokenResponse)
# async def login(body:LoginRequest, db:AsyncSession= Depends(get_db)):
#     token = await auth_service.login(db,body.email,body.password)
#     return TokenResponse(access_token=token)

@router.post("/login")
async def login(form:OAuth2PasswordRequestForm=Depends(), db:AsyncSession= Depends(get_db)):
    token = await auth_service.login(db,form.username,form.password)
    return TokenResponse(access_token=token)
