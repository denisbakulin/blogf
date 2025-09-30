from core.exceptions import AppError


class AuthError(AppError):
    """Ошибка аутентификации"""

class InvalidTokenError(AuthError):
    """Ошибка JWT"""


class InvalidPasswordError(AuthError):
    """Ошибка некорректного пароля"""
    
    def __init__(self):
        super().__init__("Некорректный пароль")
