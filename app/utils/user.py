from typing import Literal

from exceptions.auth import AuthError
from helpers.search import search_param_fabric

BANNED_USERNAME_SYMBOLS = r"""!#$%&'"()*+,-./:;<=>?@[\]^`{|}~"""
MIN_USERNAME_LENGTH = 3
MAX_USERNAME_LENGTH = 15


def ensure_correct_username(username: str) -> str:
    username = username.lower()

    if banned := (set(username) & set(BANNED_USERNAME_SYMBOLS)):
        raise AuthError(fr"В username есть запрещенные символы {banned}")

    if not (MIN_USERNAME_LENGTH <= len(username) <= MAX_USERNAME_LENGTH):
        raise AuthError(
            fr"длина username должна быть в диапазоне от "
            fr"{MIN_USERNAME_LENGTH} до {MAX_USERNAME_LENGTH}"
        )

    return username



UserSearchParams = search_param_fabric(Literal["username", "name"])






