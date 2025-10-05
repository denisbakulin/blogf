from core.exceptions import AppError


class ExternalApiRequestError(AppError):
    """Ошибка запроса от внешнего API"""

    def __init__(self, data):
        self.data = data

