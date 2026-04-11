from base.exceptions import AppError


class InsufficientAllows(AppError):
    def __init__(self, msg: str | None = None):
        super().__init__(msg or "InsufficientAllows / недостаточно прав!")