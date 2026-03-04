from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from interfaces.bot.text import START_TEXT, UNVERIFIED_TEXT
from interfaces.bot.middlewares.user_middleware import UserMiddleware, UserService
from base.db import session_maker
from entities.user import User
from interfaces.bot.keyboards.common import create_start_kb, start_kb, cancel_kb
from sqlalchemy.ext.asyncio import AsyncSession
from interfaces.bot.utils.verify import verify_user
from usecases.auth import AuthLogic
from interfaces.bot.fsm import Waiting


router = Router()

router.message.middleware(UserMiddleware(session_maker))
router.callback_query.middleware(UserMiddleware(session_maker))


async def get_code(tg_id: int, session: AsyncSession) -> str:
    auth = AuthLogic(session)
    return await auth.auth_code.create("login", tg_id)


@router.callback_query(F.data == "start")
async def start_query(callback: CallbackQuery, user: User, session: AsyncSession):
    code = await get_code(callback.from_user.id, session)

    await callback.message.edit_text(
        START_TEXT.format(name=user.username),
        reply_markup=create_start_kb(code, verified=True)
    )




@router.message(Command("start", prefix="/."))
async def start_cmd_process(
        message: Message,
        session: AsyncSession,
        user: User,
):
    params = message.text.split()

    if len(params) == 2:
        verify_code = params[1]
        success, msg = await verify_user(session, code=verify_code, tg_id=message.from_user.id)
        return await message.answer(msg)

    code = await get_code(message.from_user.id, session)

    if not user:
        await message.answer(
            START_TEXT.format(name=message.from_user.first_name) + UNVERIFIED_TEXT,
            reply_markup=create_start_kb(code, False)
        )
    else:
        await message.answer(
            START_TEXT.format(name=user.username),
            reply_markup=create_start_kb(code, True)
        )


@router.callback_query(F.data == "reset_password")
async def reset_password(
        callback: CallbackQuery,
        state: FSMContext
):

    await callback.message.answer(
        "Пожалуйста, введите новый пароль",
        reply_markup=cancel_kb
    )
    await state.set_state(Waiting.password)


@router.message(StateFilter(Waiting.password))
async def p(
        message: Message,
        state: FSMContext,
        session: AsyncSession,
        user: User
):
    auth = AuthLogic(session)
    result = await auth.set_user_password_after_forgot(user.id, message.text)
    msg = result.get("msg")
    await message.answer(msg)

    await state.clear()



@router.callback_query(F.data == "cancel")
async def remove_context(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.clear()



