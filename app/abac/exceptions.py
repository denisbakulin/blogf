from base.exceptions import AppError


class Forbidden(AppError):
    def __init__(self):
        super().__init__("Forbidden")



