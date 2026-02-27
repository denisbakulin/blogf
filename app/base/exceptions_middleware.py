from abac.exceptions import Forbidden
from base.exceptions import (EntityAlreadyExists, EntityBadRequestError,
                             EntityLockedError, EntityNotFoundError,
                             InsufficientPermissionsError)
from exceptions.auth import AuthError
from fastapi import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class ErrorResponse(JSONResponse):

    def __init__(self, status_code: status, exc: Exception):
        super().__init__(status_code=status_code, content={"detail": str(exc)})


class AppExceptionMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        try:
            return await call_next(request)

        except EntityNotFoundError as exc:
            return ErrorResponse(status.HTTP_404_NOT_FOUND, exc)

        except (EntityAlreadyExists, InsufficientPermissionsError, Forbidden) as exc:
            return ErrorResponse(status.HTTP_403_FORBIDDEN, exc)


        except EntityBadRequestError as exc:
            return ErrorResponse(status.HTTP_422_UNPROCESSABLE_ENTITY, exc)

        except AuthError as exc:
            return ErrorResponse(status.HTTP_401_UNAUTHORIZED, exc)

        except EntityLockedError as exc:
            return ErrorResponse(status.HTTP_423_LOCKED, exc)




