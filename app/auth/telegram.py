from exceptions.auth import  AuthError
from schemas.auth import  LoginTokens
from services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession

from utils.auth import TokenCreator,  ensure_correct_password, generate_auth_code
from utils.user import generate_hashed_password

from base.cache import cache
from auth.oauth import OAuthUserService, ProviderType
from auth.code import AuthCodeManager

from auth.user_create import UserCreator

class TelegramAuth:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.oauth_service = OAuthUserService(self.session)
        self.user_service = UserService(session=session)
        self.auth_code = AuthCodeManager(cache)


    def get_verify_ref(self, code: str):
        return f"https://t.me/blogf_auth_bot?start={code}"



    async def login(self, code: str, name: str) -> LoginTokens:
        tg_id = await self.auth_code.get_id("login", code)

        if not tg_id:
            raise AuthError("истекший или несуществующий код")

        user = await self.user_service.get_user_by_tg_id(int(tg_id))
        user_creator = UserCreator(self.session)

        if user is None:
            user = await user_creator.execute(name=name, username=generate_auth_code())
            await self.oauth_service.create_item(
                user_id=user.id, provider_id=tg_id, provider=ProviderType.TELEGRAM
            )

        await self.auth_code.delete("login", code)

        return TokenCreator(user.id).auth_tokens


    async def verify(
            self, code: str,
            tg_id: int,
    ):
        tg_verified = await self.oauth_service.repository.get_one_by(
            provider_id=tg_id, provider=ProviderType.TELEGRAM
        )

        if tg_verified:
            return {"status": False, "msg": "Вы уже верифицировали аккаунт через Telegram"}

        user_id = await self.auth_code.get_id("verify", code)

        if not user_id:
            return {"status": False, "msg": "Код устарел или недействителен, попробуйте еще раз!"}


        user = await self.user_service.get_user_by_id(int(user_id))

        await self.oauth_service.create_item(
            provider_id=tg_id, user_id=user.id, provider=ProviderType.TELEGRAM
        )

        await self.auth_code.delete("verify", code)

        return {"status": True, "msg": "Аккаунт успешно верифицирован!"}

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
