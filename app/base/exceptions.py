class AppError(Exception):
    """Базовая ошибка приложения"""

class LogicError(AppError):
    """Внутренняя ошибка"""


class EntityNotFoundError(AppError):
    """Ресурс не найден"""

    def __init__(
            self,
            entity: str,
            **fields
    ):
        super().__init__(
            f"{entity} "
            f"{f'с {", ".join(f"{k}={v}" for k, v in fields.items())} ' if fields else ''}"
            "не найдено!"
        )

        self.entity = entity



class EntityBadRequestError(AppError):
    """Ошибка создания/изменения ресурса"""

    def __init__(
            self,
            entity: str,
            message: str = ""
    ):
        super().__init__(
            f"[{entity}] Ошибка доступа к ресурсу "
            f"{'| ' + message if message else ''}"
        )

        self.entity = entity

class InsufficientPermissionsError(AppError):

    def __init__(self, msg: str | None = None):
        super().__init__(msg or "НЕДОСТАТОЧНО ПРАВ")

class EntityAlreadyExists(AppError):
    """Ресурс уже существует"""

    def __init__(self, entity: str, **fields):
        super().__init__(
            f"{entity} "
            f"{f'с {", ".join(f"{k}={v}" for k, v in fields.items())} ' if fields else ''}"
            "уже существует!"
        )
        self.entity = entity
        self.fields = fields


class EntityLockedError(AppError):
    """Ресурс заблокирован"""

    def __init__(self, entity: str | None = None, message: str | None = None):

        super().__init__(f"Ресурс [{entity}] заблокирован!" if not message else entity)
        self.entity = entity



from typing import Callable, Coroutine
import inspect

async def check_at_least_one_func_not_raise(options: list[tuple[Callable | Coroutine, type[Exception]]]):
    """
    Если хотя бы одна не вызывает ошибку, то не вызываем исключение,
    если все ошибочны, то выкидываем последнее
    """

    excs: list[Exception] = []

    for option, exc in options:
        try:
            if inspect.isawaitable(option):
                await option
            else:
                option()

        except exc as e:
            excs.append(e)
    print(excs)
    if len(excs) == len(options):
        raise excs[-1]


