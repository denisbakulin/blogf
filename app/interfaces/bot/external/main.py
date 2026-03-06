from faststream.redis import RedisBroker
from aiogram import Bot
from base.settings import bot_settings
from interfaces.bot.text import RESET_PASSWORD_TEXT
from interfaces.bot.keyboards.common import create_reset_password_kb


broker = RedisBroker()

bot = Bot(bot_settings.token)


@broker.subscriber("forget-password")
async def process(
        code: str,
        tg_id: int
):
    await bot.send_message(
        tg_id,
        RESET_PASSWORD_TEXT + f" http://127.0.0.1:8001/auth/reset-password?code={code}",
        parse_mode="HTML",
        reply_markup=create_reset_password_kb(code)
    )

#рассылка notify
#feedback create user main actions





