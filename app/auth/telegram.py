from auth.code import AuthCodeManager
from auth.oauth import OAuthUserService, ProviderType
from auth.user_create import UserCreator
from base.cache import cache
from base.settings import bot_settings
from exceptions.auth import AuthError
from schemas.auth import LoginTokens
from services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from utils.auth import (
    TokenCreator,
    TokenTypes,
    ensure_correct_password,
    generate_hashed_password,
    get_decoded_token,
)


class TelegramAuth:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.oauth_service = OAuthUserService(self.session)
        self.user_service = UserService(session=session)
        self.auth_code = AuthCodeManager(cache)


    def get_verify_ref(self, code: str):
        return f"https://t.me/{bot_settings.bot_name}?start={code}"


    async def login(self, token: str, name: str) -> LoginTokens:

        token_info = get_decoded_token(token)

        if token_info.type != TokenTypes.tg_login:
            raise AuthError("Неверный тип токена!")

        tg_id = await self.auth_code.get_id("used_login", token)

        if tg_id:
            raise AuthError("Код уже был использован")

        tg_id = str(token_info.user_id)

        user = await self.user_service.get_user_by_tg_id(int(tg_id))
        user_creator = UserCreator(self.session)

        if user is None:
            user = await user_creator.execute(name=name)
            await self.oauth_service.create_item(
                user_id=user.id, provider_id=tg_id, provider=ProviderType.TELEGRAM
            )
        await self.auth_code.create(type_="used_login", id_=tg_id, code=token)

        return TokenCreator(user.id).auth_tokens


    async def verify(
            self, code: str,
            tg_id: int,
    ):
        tg_verified = await self.oauth_service.repository.get_one_by(
            provider_id=tg_id, provider=ProviderType.TELEGRAM
        )

        if tg_verified:
            return {
                "status": False,
                "msg": "Вы уже верифицировали аккаунт через Telegram"
            }

        user_id = await self.auth_code.get_id("verify", code)

        if not user_id:
            return {
                "status": False,
                "msg": "Код устарел или недействителен, попробуйте еще раз!"
            }


        user = await self.user_service.get_user_by_id(int(user_id))

        await self.oauth_service.create_item(
            provider_id=tg_id, user_id=user.id, provider=ProviderType.TELEGRAM
        )

        await self.auth_code.delete("verify", code)

        return {
            "status": True,
            "msg": "Аккаунт успешно верифицирован!"
        }

    async def reset_password(self,  password: str, code: str):
        user_id = await self.auth_code.get_id("forget_password", code)

        if user_id is None:
            raise AuthError("Истекший код!")

        await self.user_service.get_by_or_raise(id=user_id)

        ensure_correct_password(password)
        password = generate_hashed_password(password)

        await self.user_service.update_item(int(user_id), password=password)
        await self.auth_code.delete("forget_password", code)

        return {"status": True, "msg": "Пароль успешно обновлен"}
