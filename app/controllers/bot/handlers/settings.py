from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from base.db import session_maker
from controllers.bot.fsm import ChangeFSM
from controllers.bot.keyboards.common import ChangeCallback, cancel_kb, settings_kb
from controllers.bot.middlewares.user_middleware import UserMiddleware
from controllers.bot.text import create_settings_text
from controllers.bot.utils.settings import process_change as process_user_change
from services.user import User, UserService
from html import escape

router = Router()
router.callback_query.middleware(UserMiddleware(session_maker))
router.message.middleware(UserMiddleware(session_maker))

@router.callback_query(F.data == "settings")
async def settings_menu(
        callback: CallbackQuery,
        user: User,
        user_service: UserService,
):
    """Главное меню настроек"""

    profile = await user_service.profile_service.get_by_or_raise(user_id=user.id)

    await callback.message.edit_text(
        create_settings_text(user=user, profile=profile),
        reply_markup=settings_kb
    )


def get_state(callback_data: ChangeCallback) -> tuple[ChangeFSM, str]:

    return {
        callback_data.name: (ChangeFSM.name, "name"),
        callback_data.username: (ChangeFSM.username, "username"),
        callback_data.bio: (ChangeFSM.bio, "bio"),
    }[True]

@router.callback_query(ChangeCallback.filter())
async def settings_menu(
        callback: CallbackQuery,
        callback_data: ChangeCallback,
        state: FSMContext
):
    state_, type_ = get_state(callback_data)

    await state.set_state(state_)
    await callback.message.answer("Введите " + type_, reply_markup=cancel_kb)

@router.message(StateFilter(ChangeFSM))
async def process_change(
        message: Message,
        state: FSMContext,
        user: User,
        user_service: UserService
):
    change = message.text
    status, msg = await process_user_change(change, user, state, user_service)

    if status:
        await state.clear()

    await message.reply(escape(msg))



