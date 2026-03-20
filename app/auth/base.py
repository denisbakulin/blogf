from datetime import datetime

from auth.code import AuthCodeManager
from base.broker import broker
from base.cache import cache
from entities.user import User
from exceptions.auth import AuthError, InvalidPasswordError
from schemas.auth import AuthCreds, LoginTokens, PasswordChange
from services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from utils.auth import (
    TokenCreator,
    ensure_correct_password,
    generate_hashed_password,
    verify_password,
)


class BaseAuth:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_service = UserService(session=session)
        self.auth_code = AuthCodeManager(cache)

    async def login(self, creds: AuthCreds, host: str) -> LoginTokens:

        user = await self.user_service.get_by_or_raise(username=creds.username)

        if user.password is None:
            raise AuthError("Пароль не установлен")

        if not verify_password(creds.password, user.password):

            raise InvalidPasswordError()

        await broker.publish({
            "author_id": user.id,
            "host": host,
            "time": datetime.now(),
        },"new-login")

        return TokenCreator(user.id).auth_tokens



    async def change_password(self, user: User, pwd: PasswordChange):
        ensure_correct_password(pwd.new_password)

        # Если пароль не установлен
        if (user.password, pwd.old_password) == (None, None):
            password = generate_hashed_password(pwd.new_password)
            return await self.user_service.update_item(user.id, password=password)

        if not verify_password(pwd.old_password, user.password):
            raise InvalidPasswordError()

        password = generate_hashed_password(pwd.new_password)

        await self.user_service.update_item(user.id, password=password)


    async def forget_password(self, username: str):

        user = await self.user_service.get_user_by_username(username)
        code = await self.auth_code.create( "forget_password", user.id)

        await broker.publish({
            "code": code,
            "author_id": user.id},
        "forget-password"
        )
