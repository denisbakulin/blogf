from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from interfaces.bot.text import START_TEXT, UNVERIFIED_TEXT, PASSWORD_RULES_TEXT
from interfaces.bot.middlewares.user_middleware import UserMiddleware
from base.db import session_maker
from entities.user import User
from interfaces.bot.keyboards.common import create_start_kb,  cancel_kb, CodeCallback
from sqlalchemy.ext.asyncio import AsyncSession
from interfaces.bot.utils.verify import verify_user
from auth.telegram import TelegramAuth
from interfaces.bot.fsm import WaitingFSM
from exceptions.auth import AuthError


router = Router()

router.message.middleware(UserMiddleware(session_maker))
router.callback_query.middleware(UserMiddleware(session_maker))


async def get_code(tg_id: int, session: AsyncSession) -> str:
    auth = TelegramAuth(session)
    return await auth.auth_code.create("login", tg_id)


@router.callback_query(F.data == "menu")
async def menu_query(callback: CallbackQuery, user: User, session: AsyncSession):
    code = await get_code(callback.from_user.id, session)

    await callback.message.edit_text(
        START_TEXT.format(name=user.username),
        reply_markup=create_start_kb(
             code=code, verified=True
        )
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

    code = await get_code(message.from_user.id, session)


    if not user:

        await message.answer(
            START_TEXT.format(name=message.from_user.first_name) + UNVERIFIED_TEXT,
            reply_markup=create_start_kb(
                name=message.from_user.first_name, code=code, verified=False
            )
        )
    else:
        await message.answer(
            START_TEXT.format(name=user.username),
            reply_markup=create_start_kb(
                code=code, verified=True
            )
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
    await state.clear()



