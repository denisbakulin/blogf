from aiogram import F, Router
from aiogram.types import CallbackQuery

from base.db import session_maker
from interfaces.bot.keyboards.common import notify_kb
from interfaces.bot.middlewares.user_middleware import UserMiddleware

router = Router()
router.callback_query.middleware(UserMiddleware(session_maker))


@router.callback_query(F.data == "notifications")
async def notifications_callback(
        callback: CallbackQuery,
):

    await callback.message.edit_text(
        "Меню уведомлений",
        reply_markup=notify_kb
    )

