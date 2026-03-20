from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from base.db import session_maker
from base.exceptions import AppError
from entities.user import User
from controllers.bot.fsm import CreatePostFSM
from controllers.bot.keyboards.common import cancel_kb, create_inline_kb
from controllers.bot.middlewares.user_middleware import UserMiddleware
from controllers.bot.text import ENTER_POST_CONTENT_TEXT, ENTER_POST_TITLE_TEXT
from controllers.bot.utils.post import ensure_correct_content, ensure_correct_title
from sqlalchemy.ext.asyncio import AsyncSession
from usecases.post import CreateWallPostUseCase, PostBase

router = Router()

router.message.middleware(UserMiddleware(session_maker))
router.callback_query.middleware(UserMiddleware(session_maker))



@router.callback_query(F.data == "create_post")
async def create_post(
        callback: CallbackQuery,
        state: FSMContext
):
    await state.set_state(CreatePostFSM.title)
    await callback.message.answer("Создание поста", reply_markup=cancel_kb)
    await callback.message.answer(ENTER_POST_TITLE_TEXT)


@router.message(StateFilter(CreatePostFSM.title))
async def enter_post_title(
        message: Message,
        state: FSMContext
):
    title = message.text
    try:
        ensure_correct_title(title)
        await state.set_state(CreatePostFSM.content)
        await state.update_data({"title": title})
        await message.answer(ENTER_POST_CONTENT_TEXT)
    except AppError:
        await message.reply("❌ Проверьте корректность заголовка и попробуйте снова")



@router.message(StateFilter(CreatePostFSM.content))
async def enter_post_content(
        message: Message,
        state: FSMContext,
        session: AsyncSession,
        user: User
):
    try:
        content = message.text
        ensure_correct_content(content)
        data = await state.get_data()

        wpc = CreateWallPostUseCase(session)
        post = await wpc.execute(user.id, PostBase(title=data["title"], content=content))

        await message.answer(
            f"✅ <b>Пост успешно создан!</b>\n",
            reply_markup=create_inline_kb(**{
                "Открыть пост": f"http://127.0.0.1:8000/posts/{post.slug}"
            })
        )
        await state.clear()
    except AppError:
        await message.answer("❌ Проверьте корректность содержания и попробуйте снова" )







