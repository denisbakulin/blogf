import asyncio

import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from aiogram.types import BotCommand

from base.settings import bot_settings
from base.cache import init_fastapi_cache as init_cache

from interfaces.bot.fsm import storage
from interfaces.bot.handlers.common import router as cmd_router
from interfaces.bot.handlers.profile import router as profile_router


import logging
logging.basicConfig(level=logging.DEBUG)


dp = Dispatcher(storage=storage)

bot = Bot(
    token=bot_settings.token,
    default=DefaultBotProperties(
        parse_mode='HTML'
    ),
)


cmd_menu = [
    ("/start", "Start work / login "),
]


def get_cmd_menu(
    cmd_list: list[tuple[str, str]]
) -> list[BotCommand]:
    return [
        BotCommand(command=command, description=description)
        for command, description in cmd_list
    ]
from interfaces.bot.external.main import broker

async def main() -> None:

    init_cache()

    dp.include_routers(
        cmd_router,
        profile_router,
    )
    await bot.set_my_commands(get_cmd_menu(cmd_menu))

    await bot.delete_webhook(drop_pending_updates=True)
    await broker.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

