from aiogram import Bot
from faststream.redis import RedisBroker

from base.settings import bot_settings
from interfaces.bot.keyboards.common import create_reset_password_kb
from interfaces.bot.text import RESET_PASSWORD_TEXT
from datetime import datetime
from faststream import Depends
from base.db import get_session, AsyncSession
from auth.telegram import TelegramAuth, ProviderType
from httpx import AsyncClient

broker = RedisBroker()

bot = Bot(bot_settings.token)


@broker.subscriber("forget-password")
async def forget_password(
        code: str,
        user_id: int,
        session: AsyncSession = Depends(get_session)
):
    auth = TelegramAuth(session)
    tg_oauth = await auth.oauth_service.get_by_or_raise(
        user_id=user_id, provider=ProviderType.TELEGRAM
    )
    tg_id = int(tg_oauth.provider_id)
    await bot.send_message(
        tg_id,
        RESET_PASSWORD_TEXT + f" http://127.0.0.1:8000/auth/reset-password?code={code}",
        parse_mode="HTML",
        reply_markup=create_reset_password_kb(code)
    )

@broker.subscriber("new-login")
async def notify_login(
        user_id: int,
        host: str,
        time: datetime,
        session: AsyncSession = Depends(get_session)
):
    # сделать норм обертку
    auth = TelegramAuth(session)

    tg_oauth = await auth.oauth_service.get_by_or_raise(
        user_id=user_id, provider=ProviderType.TELEGRAM
    )

    tg_id = int(tg_oauth.provider_id)
    text = ""

    async with AsyncClient() as ac:
        response = await ac.get(f"http://ipwho.is/{host}?lang=ru")
        host_info = response.json()

        success = host_info.get("success", False)

        if not success:
            text += host_info.get("message")
        else:
            text += host_info.get("country")
            text += host_info.get("flag", {}).get("emoji") + "\n"
            text += host_info.get("region") + "\n"
            text += host_info.get("city") + "\n"



    await bot.send_message(
        tg_id,
        (f"🔔 <p>Новое подключение к аккаунту по паролю</p>\n"
         f"🌐 IP адрес: {host}\n"
         f"🕐 Время: {time.strftime('%d.%m.%Y %H:%M:%S')}\n{text}"
         ),
        parse_mode="HTML"
    )






