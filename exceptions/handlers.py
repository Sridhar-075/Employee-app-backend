from exceptions import AppException, BadRequestException, ConflictException, NotFoundException,UnauthorizedException,ForbiddenException
from fastapi import status, Request
from fastapi.responses import JSONResponse
import logging
import json
from fastapi import FastAPI

logger = logging.getLogger(__name__)
_STATUS_MAP: dict[type[AppException],int] = {
    NotFoundException:status.HTTP_404_NOT_FOUND,
    ConflictException:status.HTTP_409_CONFLICT,
    BadRequestException:status.HTTP_400_BAD_REQUEST,
    UnauthorizedException: status.HTTP_401_UNAUTHORIZED,
    ForbiddenException:status.HTTP_403_FORBIDDEN
}


def register_exception_handler(app:FastAPI):
    @app.exception_handler(AppException)
    async def app_exception_handler(request:Request, exc:AppException):
        code = _STATUS_MAP.get(type(exc),status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JSONResponse(
            status_code = code,
            content= {"detail":str(exc.detail)}
        )