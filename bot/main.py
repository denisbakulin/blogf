import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from check import check_verify_code
from text import AUTH_TEXT

from app.base.settings import tg_bot_settings


class Waiting(StatesGroup):
    code = State()

bot = Bot(
    token=tg_bot_settings.token,
    default=DefaultBotProperties(parse_mode='HTML')
)

dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer(AUTH_TEXT.format(name=message.from_user.first_name))
    await state.set_state(Waiting.code)

@dp.message()
async def try_code(message: Message, state: FSMContext):

    response = await check_verify_code(message.text, message.from_user.id)
    msg = response.get("msg") or "err"

    if response.get("status"):
        await message.reply(msg)
        await state.clear()
    else:
        await message.reply(msg)

async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())