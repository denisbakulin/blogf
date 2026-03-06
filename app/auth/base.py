from exceptions.auth import InvalidPasswordError, AuthError
from schemas.auth import AuthCreds, LoginTokens, PasswordChange
from services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession


from utils.user import verify_password, generate_hashed_password
from entities.user import User
from base.broker import broker

from auth.oauth import OAuthUserService, ProviderType
from utils.auth import ensure_correct_password, TokenCreator
from auth.code import AuthCodeManager
from base.cache import cache


class BaseAuth:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_service = UserService(session=session)
        self.auth_code = AuthCodeManager(cache)



    async def login(self, creds: AuthCreds) -> LoginTokens:


        user = await self.user_service.get_by_or_raise(username=creds.username)

        if user.password is None:
            raise AuthError("Пароль не установлен")

        if not verify_password(creds.password, user.password):

            raise InvalidPasswordError()

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
        oauth_service = OAuthUserService(self.session)

        tg = await oauth_service.get_by_or_raise(
            user_id=user.id, provider=ProviderType.TELEGRAM
        )

        await broker.publish({
            "code": code,
            "tg_id": tg.provider_id},
        "forget-password"
        )
