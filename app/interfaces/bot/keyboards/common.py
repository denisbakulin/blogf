from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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


start_kb = create_inline_kb(**{
    "Меню": "start"
})

reset_password_kb = create_inline_kb(**{
    "Восстановить пароль": "reset_password"
})

cancel_kb = create_inline_kb(**{
    "Отмена": {
        "callback_data": "cancel",
        "style": "danger"
    }
})

def create_start_kb(code: str, verified: bool):
    kb_data = {}

    if verified:
        kb_data["👤 Мой Профиль"] = "profile"

    kb_data["🔑 Войти в Blogf"] = f"http://127.0.0.1:8001/auth/telegram/login?code={code}"

    return create_inline_kb(width=1, **kb_data)


