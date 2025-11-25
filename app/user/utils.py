from typing import Literal

from passlib.context import CryptContext

from helpers.search import search_param_fabric

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",

)


def verify_password(password, hashed_password) -> bool:
    return pwd_context.verify(password, hashed_password)



def generate_hashed_password(password) -> str:
    password_bytes = password.encode('utf-8')

    # Если пароль длиннее 72 байтов - обрезаем его
    if len(password_bytes) > 72:
        password = password_bytes[:72].decode('utf-8', 'ignore')

    return pwd_context.hash(password)


UserSearchParams = search_param_fabric(Literal["username", "id"])



