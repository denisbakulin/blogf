from entities.user import User, Profile
from aiogram import html

START_TEXT = (
    "👋 <b>Здравствуйте, {name}!</b>\n\n"
)

UNVERIFIED_TEXT = (
    "1️⃣ Если вы хотите <b>зарегистрироваться</b> или войти через Telegram — нажмите на кнопку ниже.\n"
    "2️⃣ Если вы хотите <b>верифицировать</b> существующий аккаунт, пожалуйста, перейдите в личный кабинет на нашем сайте."
)

PASSWORD_RULES_TEXT = (
    "🔐 Пожалуйста, введите новый пароль\n\n"
    "Требования к паролю:\n"
    "• Минимум 8 символов\n"
    "• Хотя бы одна заглавная буква\n"
    "• Хотя бы одна строчная буква\n"
    "• Хотя бы одна цифра\n"
)

RESET_PASSWORD_TEXT = (
    "🔐 <b>Запрос смены пароля</b>\n\n"
    "Кто-то хочет сменить пароль в твоем аккаунте Blogf.\n\n"
    "👉 <b>Если это ты:</b>\n"
    "Жми кнопку ниже или на ссылку (действительна 10 минут).\n\n"
    "🚫 <b>Если не ты:</b>\n"
    "Просто проигнорируй. Пароль остался прежним."
)


def get_profile_text(user: User, profile: Profile) -> str:
    username = html.quote(user.username)
    name = html.bold(html.quote(user.name or "Не указано"))
    bio = html.italic(html.quote(profile.bio or "Информация отсутствует"))
    city = html.quote(profile.city or "Не указан")

    verify_icon = "🏷 <b>Верифицирован</b>" if user.is_verified else "⚪️ <b>Обычный аккаунт</b>"
    active_icon = "🟢 <b>Активен</b>" if user.is_active else "🔴 <b>Заблокирован</b>"

    text = [
        f"👤 <b>ЛИЧНЫЙ КАБИНЕТ</b>",
        f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
        f"<b>user_id:</b> <code>{user.id}</code>",
        f"<b>Username:</b> {username}",
        f"<b>Имя:</b> {name}",
        f"<b>Город:</b> {city}",
        f"<b>Возраст:</b> {profile.age or '—'}",
        f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
        f"📝 <b>О себе:</b>",
        f"{bio}",
        f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
        f"🛡 <b>Статус:</b> {verify_icon}",
        f"⚙️ <b>Доступ:</b> {active_icon}",
        f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯",
        f"📅 <i>В системе с {user.created_at.strftime('%d.%m.%Y')}</i>"
    ]

    return "\n".join(text)
