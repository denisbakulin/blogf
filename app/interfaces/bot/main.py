import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import BaseFilter
from aiogram.types import BotCommand, CallbackQuery

from base.cache import init_fastapi_cache as init_cache
from base.settings import bot_settings
from interfaces.bot.external.main import broker
from interfaces.bot.fsm import storage

logging.basicConfig(level=logging.DEBUG)


dp = Dispatcher(storage=storage)

bot = Bot(
    token=bot_settings.token,
    default=DefaultBotProperties(
        parse_mode='HTML'
    ),
)


class AnswerCallback(BaseFilter):
    """Ответ на callback"""

    async def __call__(self, callback: CallbackQuery, *args, **kwargs):
        await callback.answer()
        return True


# Отвечает на все калбеки
dp.callback_query.filter(AnswerCallback())

cmd_menu = [
    ("/start", "Войти в Blogf 🔑"),
]

def get_cmd_menu(
    cmd_list: list[tuple[str, str]]
) -> list[BotCommand]:
    return [
        BotCommand(command=command, description=description)
        for command, description in cmd_list
    ]


from interfaces.bot.handlers import *

dp.include_routers(
    auth_router,
    notifications_router,
    profile_router,
    settings_router,
    post_router
)

async def main() -> None:

    init_cache()


    await bot.set_my_commands(get_cmd_menu(cmd_menu))

    await bot.delete_webhook(drop_pending_updates=True)
    await broker.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

