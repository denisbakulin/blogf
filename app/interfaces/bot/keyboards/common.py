from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class CodeCallback(CallbackData, prefix="reset-pwd-code"):
    code: str


class ChangeCallback(CallbackData, prefix="change"):
    username: bool = False
    name: bool = False
    bio: bool = False



def create_inline_kb(width: int = 1, **kwargs) -> InlineKeyboardMarkup:
    """
    Универсальная функция для создания инлайн-клавиатур.
    :param width: Кол-во кнопок в ряду.
    :param kwargs: Текст кнопки = callback_data (или dict для ссылок).
    """
    builder = InlineKeyboardBuilder()
    buttons = []

    for text, data in kwargs.items():
        if isinstance(data, str) and data.startswith(('http://', 'https://')):
            buttons.append(InlineKeyboardButton(text=text, url=data))
        else:
            # Если передана строка — это callback_data
            # Если нужен стиль или эмодзи, можно передать dict (см. пример ниже)
            if isinstance(data, dict):
                buttons.append(InlineKeyboardButton(text=text, **data))
            else:
                buttons.append(InlineKeyboardButton(text=text, callback_data=data))

    builder.add(*buttons)
    builder.adjust(width)
    return builder.as_markup()


menu_kb = create_inline_kb(**{
    "☰ Меню": "menu"
})

from entities.notification import Notification, NotificationType


def mapper_notify(n: NotificationType) -> str:
    return {
        NotificationType.NEW_POST: "Новый пост",
        NotificationType.BASE_LOGIN: "Логин по паролю"
    }[n]


def create_notify_kb(notifications: list[Notification]):
    buttons = {}
    user_notify = [i.type for i in notifications]

    for n in NotificationType:
        text = mapper_notify(NotificationType(n))
        if n in user_notify:
            buttons[f"✅ {text}"] = n
        else:
            buttons[f"❌ {text}"] = n

    return create_inline_kb(**{
        **buttons,
        "☰ Меню": "menu"
    })



profile_kb = create_inline_kb(**{
    "⚙️ Настройки": "settings",
    "✏️ Создать пост": "create_post",
    "☰ Меню": "menu",
})

settings_kb = create_inline_kb(**{
    "👤 Изменить name": ChangeCallback(name=True).pack(),
    "@ Изменить username": ChangeCallback(username=True).pack(),
    "📝 Изменить bio": ChangeCallback(bio=True).pack(),
    "☰ Меню": "menu"
})

def create_reset_password_kb(code: str) -> InlineKeyboardMarkup:
    return create_inline_kb(**{
    "🔄 Восстановить пароль": CodeCallback(code=code).pack()
})

cancel_kb =  create_inline_kb(**{
    "Отмена": {
        "callback_data": "cancel",
        "style": "danger"
    }
})

def create_login_ref(name: str, token : str) -> str:
    """Ссылка на логин через telegram"""
    name = name or "Anonymous"

    return f"http://127.0.0.1:5173/auth/telegram/login?token={token}&name={name}"

def create_start_kb( token: str, verified: bool, name: str | None = None):
    kb_data = {}

    if verified:
        kb_data["👤 Мой Профиль"] = "profile"
        kb_data["🔔 Уведомления"] = "notifications"

    kb_data["🔑 Войти в Blogf"] = create_login_ref(name, token)

    return create_inline_kb(width=2, **kb_data)


