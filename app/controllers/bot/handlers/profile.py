from aiogram import F, Router
from aiogram.types import CallbackQuery
from base.db import session_maker
from controllers.bot.keyboards.common import profile_kb
from controllers.bot.middlewares.user_middleware import UserMiddleware
from controllers.bot.text import get_profile_text
from services.user import User, UserService

router = Router()
router.callback_query.middleware(UserMiddleware(session_maker))


@router.callback_query(F.data == "profile")
async def profile_callback(
        callback: CallbackQuery,
        user: User,
        user_service: UserService,
):
    profile = await user_service.get_user_profile(user)

    await callback.message.edit_text(
        get_profile_text(user, profile),
        reply_markup=profile_kb
    )




