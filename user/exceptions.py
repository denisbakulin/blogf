class UserAlreadyExistErr(Exception):
    ...

class UserNotFoundErr(Exception):
    ...


class UserNotVerifiedErr(Exception):
    ...


class UserInactiveErr(Exception):
    ...


class IncorrectPasswordErr(Exception):
    ...