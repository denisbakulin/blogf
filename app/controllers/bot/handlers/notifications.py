from aiogram import F, Router
from aiogram.types import CallbackQuery
from base.db import AsyncSession, session_maker
from entities.user import User
from controllers.bot.keyboards.common import create_notify_kb
from controllers.bot.middlewares.user_middleware import UserMiddleware
from services.notification import NotificationService, NotificationType

router = Router()
router.callback_query.middleware(UserMiddleware(session_maker))

@router.callback_query(F.data == "notifications")
async def notifications_callback(
        callback: CallbackQuery,
        session: AsyncSession,
        user: User
):
    """Показывает меню нотификаций"""

    serv = NotificationService(session)
    notifications = await serv.repository.get_any_by(user_id=user.id)

    await callback.message.edit_text(
        "Меню уведомлений",
        reply_markup=create_notify_kb(notifications)
    )


@router.callback_query(F.data.in_(NotificationType))
async def process_notification_button(
        callback: CallbackQuery,
        session: AsyncSession,
        user: User
):
    """Включает/выключает уведомления"""

    serv = NotificationService(session)
    await serv.process(
        user_id=user.id,
        type_=NotificationType(callback.data)
    )
    notifications = await serv.repository.get_any_by(user_id=user.id)
    await callback.message.edit_text(
        "Меню уведомлений",
        reply_markup=create_notify_kb(notifications)
    )