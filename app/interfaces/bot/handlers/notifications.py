from aiogram.types import  CallbackQuery
from aiogram import Router, F
from services.user import UserService, User
from interfaces.bot.middlewares.user_middleware import UserMiddleware
from base.db import session_maker
from interfaces.bot.keyboards.common import start_kb

router = Router()
router.callback_query.middleware(UserMiddleware(session_maker))


@router.callback_query(F.data == "notifications")
async def notifications_callback(
        callback: CallbackQuery,
):

    await callback.message.edit_text(
        "тут нотификации",
        reply_markup=start_kb
    )

