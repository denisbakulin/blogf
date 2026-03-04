from typing import Awaitable, Any, Callable
from aiogram.types import TelegramObject
from aiogram import BaseMiddleware


class SessionMiddleware(BaseMiddleware):
    """
    middleware для получения сессии AsyncSession
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
            data["session"] = session
            return await handler(event, data)