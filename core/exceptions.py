from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import status as st
from core.log import logger

class AppError(Exception):
    """Базовая ошибка приложения"""


class EntityNotFoundError(AppError):
    """Ресурс не найден"""

    def __init__(
            self,
            entity: str,
            entity_id: int = None,
            fields: dict = None,
    ):
        super().__init__(
            f"{entity} "
            f"{f'с id={entity_id} ' if entity_id else ''}"
            f"{f'с {", ".join(f"{k}={v}" for k, v in fields.items())} ' if fields else ''}"
            "не найдено!"
        )

        self.entity = entity
        self.entity_id = entity_id


class EntityAlreadyExists(AppError):
    """Ресурс уже существует"""

    def __init__(self, entity: str, field: str,  value):
        super().__init__(f"{entity} с {field}={value} уже существует!")
        self.entity = entity
        self.field = field
        self.value = value


class EntityLockedError(AppError):
    """Ресурс заблокирован"""

    def __init__(self, entity: str):
        super().__init__(f"Ресурс [{entity}] заблокирован!")
        self.entity = entity

class InvalidTokenError(AppError):
    """Ошибка JWT"""


def init_error_handlers(app: FastAPI):

    @app.exception_handler(EntityNotFoundError)
    async def handler_not_found_error(_, exc: EntityNotFoundError) -> JSONResponse:
        return JSONResponse(
            status_code=st.HTTP_404_NOT_FOUND,
            content={
                "detail": str(exc),
            }
        )

    @app.exception_handler(EntityAlreadyExists)
    async def handler_already_exists_error(_, exc: EntityAlreadyExists) -> JSONResponse:
        return JSONResponse(
            status_code=st.HTTP_403_FORBIDDEN,
            content={
                "detail": str(exc),
            }
        )

    @app.exception_handler(InvalidTokenError)
    async def handler_invalid_token_error(_, exc: InvalidTokenError) -> JSONResponse:
        return JSONResponse(
            status_code=st.HTTP_401_UNAUTHORIZED,
            content={
                "detail": str(exc),
            }
        )

    @app.exception_handler(EntityLockedError)
    async def handler_locked_entity_error(_, exc: EntityLockedError) -> JSONResponse:
        return JSONResponse(
            status_code=st.HTTP_423_LOCKED,
            content={
                "detail": str(exc),
            }
        )







