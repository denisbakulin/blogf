from base.exceptions import AppError


class Forbidden(AppError):
    def __init__(self, msg: str | None = None):
        super().__init__(msg or "Forbidden")



