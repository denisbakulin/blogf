from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from services.user import UserService


class UserMiddleware(BaseMiddleware):
    """
    middleware для получения текущего
    верифицированного пользователя User
    и UserService
    """

    def __init__(self, session_maker):
        self.session_maker = session_maker

    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        async with self.session_maker() as session:
            user_service = UserService(session)
            user = await user_service.get_user_by_tg_id(tg_id=event.from_user.id)

            data["user"] = user
            data["session"] = session
            data["user_service"] = user_service

            return await handler(event, data)