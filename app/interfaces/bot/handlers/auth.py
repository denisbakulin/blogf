from aiogram import F, Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from auth.telegram import TelegramAuth
from base.db import session_maker
from entities.user import User
from exceptions.auth import AuthError
from interfaces.bot.fsm import WaitingFSM
from interfaces.bot.keyboards.common import (CodeCallback, cancel_kb,
                                             create_start_kb)
from interfaces.bot.middlewares.user_middleware import UserMiddleware
from interfaces.bot.text import (PASSWORD_RULES_TEXT, START_TEXT,
                                 UNVERIFIED_TEXT)
from interfaces.bot.utils.verify import verify_user
from utils.auth import TokenCreator

router = Router()

router.message.middleware(UserMiddleware(session_maker))
router.callback_query.middleware(UserMiddleware(session_maker))


def get_login_token(tg_id: int) -> str:
    return TokenCreator(tg_id).tg_login

@router.callback_query(F.data == "menu")
async def menu_query(callback: CallbackQuery, user: User):
    token = get_login_token(callback.from_user.id)

    await callback.message.edit_text(
        START_TEXT.format(name=user.username),
        reply_markup=create_start_kb(token=token, verified=True)
    )


@router.message(Command("start", prefix="/."))
async def start_cmd_process(
        message: Message,
        session: AsyncSession,
        user: User,
):
    start_cmd = message.text.split()

    if len(start_cmd) == 2:
        _, verify_code = start_cmd
        success, msg = await verify_user(
            session, code=verify_code, tg_id=message.from_user.id
        )
        return await message.answer(msg)

    token = get_login_token(message.from_user.id)

    if not user:
        await message.answer(
            START_TEXT.format(name=message.from_user.first_name) + UNVERIFIED_TEXT,
            reply_markup=create_start_kb(token=token, verified=False, name=message.from_user.first_name)
        )
    else:
        await message.answer(
            START_TEXT.format(name=user.username),
            reply_markup=create_start_kb(token=token, verified=True)
        )


@router.callback_query(CodeCallback.filter())
async def callback_reset_password(
        callback: CallbackQuery,
        state: FSMContext,
        callback_data: CodeCallback,
        session: AsyncSession
):
    auth = TelegramAuth(session)

    code = await auth.auth_code.get_id("forget_password", callback_data.code)

    if code is None:
        return await callback.message.answer(
       "❌ Истекший код"
    )

    await callback.message.answer(
        PASSWORD_RULES_TEXT,
        reply_markup=cancel_kb
    )

    await state.set_data({"code": callback_data.code})
    await state.set_state(WaitingFSM.password)


@router.message(StateFilter(WaitingFSM.password))
async def process_reset_password(
        message: Message,
        state: FSMContext,
        session: AsyncSession,
):
    data = await state.get_data()
    code = data["code"]

    auth = TelegramAuth(session)

    try:
        result = await auth.reset_password(message.text, code)
    except AuthError as e:
        return await message.answer(str(e))

    status = result.get("status")
    msg = ("✅ " if status else "❌ ") + result.get("msg")

    await message.reply(msg)
    if status:
        await state.clear()


@router.callback_query(F.data == "cancel")
async def remove_context(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer("❗️ Действие отменено")
    await state.clear()



