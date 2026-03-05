from base.exceptions import AppError


class AuthError(AppError):
    """Ошибка аутентификации"""

class InvalidTokenError(AuthError):
    """Ошибка JWT"""



class InvalidPasswordError(AuthError):
    """Ошибка некорректного пароля"""

    def __init__(self, message: str | None = None):
        super().__init__(message or "Некорректный пароль")
