from datetime import datetime

from aiogram import Bot
from auth.telegram import ProviderType, TelegramAuth
from base.db import AsyncSession, get_session
from base.settings import bot_settings
from controllers.bot.keyboards.common import create_reset_password_kb
from controllers.bot.text import RESET_PASSWORD_TEXT
from controllers.bot.utils.whois import ipWhoIsManager
from faststream import Depends
from faststream.redis import RedisBroker
from services.notification import NotificationService, NotificationType

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
    notify = NotificationService(session)
    await notify.get_by_or_raise(type=NotificationType.BASE_LOGIN, user_id=user_id)

    auth = TelegramAuth(session)

    tg_oauth = await auth.oauth_service.get_by_or_raise(
        user_id=user_id, provider=ProviderType.TELEGRAM
    )

    tg_id = int(tg_oauth.provider_id)

    text = await ipWhoIsManager().get_host_info(host)

    await bot.send_message(
        tg_id,
        (f"<b>🔔 Новое подключение к аккаунту по паролю</b>\n"
         f"🌐 IP адрес: {host}\n"
         f"🕐 Время: {time.strftime('%d.%m.%Y %H:%M:%S')}\n{text}"
         ),
        parse_mode="HTML"
    )






