from aiogram.types import  CallbackQuery
from aiogram import Router, F
from interfaces.bot.text import get_profile_text
from services.user import UserService, User
from interfaces.bot.middlewares.user_middleware import UserMiddleware
from base.db import session_maker, AsyncSession
from interfaces.bot.keyboards.common import start_kb
router = Router()
router.callback_query.middleware(UserMiddleware(session_maker))



@router.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery, user: User, user_service: UserService, session: AsyncSession):

    if not user: return

    profile = await user_service.get_user_profile(user)

    await callback.message.edit_text(
        get_profile_text(user, profile),
        reply_markup=start_kb
    )

