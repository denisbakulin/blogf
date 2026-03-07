from aiogram.types import  CallbackQuery
from aiogram import Router, F
from interfaces.bot.middlewares.user_middleware import UserMiddleware
from base.db import session_maker
from interfaces.bot.keyboards.common import menu_kb

router = Router()
router.callback_query.middleware(UserMiddleware(session_maker))


@router.callback_query(F.data == "notifications")
async def notifications_callback(
        callback: CallbackQuery,
):

    await callback.message.edit_text(
        "тут нотификации",
        reply_markup=menu_kb
    )

