import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from text import VERIFY_TEXT, START_TEXT

from settings import bot_settings
from fs import broker

class Waiting(StatesGroup):
    code = State()


dp = Dispatcher()
bot = Bot(
    token=bot_settings.token,
    default=DefaultBotProperties(parse_mode='HTML'),
)
import logging
logging.basicConfig(level=logging.DEBUG)



@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(START_TEXT.format(name=message.from_user.first_name))

@dp.message(Command("verify"))
async def verify(message: Message, state: FSMContext):
    await message.answer(VERIFY_TEXT)
    await state.set_state(Waiting.code)


@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await message.answer(AUTH_TEXT.format(name=message.from_user.first_name))
    await state.set_state(Waiting.code)

@dp.message()
async def try_code(message: Message, state: FSMContext):
    print({"code": message.text, "tg_id": message.from_user.id})
    response = await broker.request(
        {"code": message.text, "tg_id": message.from_user.id}, "tg-verification"
    )

    data = await response.decode()
    success = data.get("status", False)
    msg = data.get("msg", "default")

    if success:
        await message.reply(msg)
        await state.clear()
    else:
        await message.reply(msg)


async def main() -> None:
    await broker.start()
    await bot.delete_webhook(drop_pending_updates=True)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())