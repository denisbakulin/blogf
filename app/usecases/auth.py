from typing import Literal

from exceptions.auth import InvalidPasswordError, AuthError
from schemas.auth import AuthCreds, LoginTokens, PasswordChange, TgAuthCode, TgLoginAnswer
from services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate
from utils.auth import TokenCreator, generate_auth_code, check_password
from utils.user import verify_password, generate_hashed_password
from entities.user import User
from base.broker import broker
from typing import TypeAlias
from base.cache import cache, Redis
from services.container import ContainerService, ContainerType

from deps.tg_verified import TgVerifiedService

codeType: TypeAlias = Literal["login", "verify", "forget_password"]

def ensure_correct_password(pwd: str):
    is_pwd_correct, msg = check_password(pwd)
    if not is_pwd_correct:
        raise InvalidPasswordError(msg)

class AuthCode:
    def __init__(self, redis: Redis, prefix: str = "tg", ttl: int = 600):
        self.cache = redis
        self.prefix = prefix
        self.ttl = ttl


    async def create(self, type_: codeType, id_: int) -> str:
        code = generate_auth_code()
        await self.cache.set(
            f"{self.prefix}:code:{type_}:{code}", id_, ex=self.ttl
        )
        return code

    async def get_id(self, type_: codeType, code: str) -> int | None:
        response = await self.cache.get(f"{self.prefix}:code:{type_}:{code}")
        return int(response) if response is not None else None


    async def delete(self, type_: codeType, code: str) -> None:
        await self.cache.delete(f"{self.prefix}:code:{type_}:{code}")


def _create_auth_tokens(user_id: int) -> LoginTokens:
    tokens = TokenCreator(user_id)

    return LoginTokens(
        access=tokens.access,
        refresh=tokens.refresh
    )


class TelegramAuth:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_service = UserService(session=session)
        self.auth_code = AuthCode(cache)

    async def register(self, user: UserCreate, code: str) -> LoginTokens:

        tg_id = await self.auth_code.get_id("login", code)
        tgv_service = TgVerifiedService(self.session)
        verified = await tgv_service.repository.get_one_by(tg_id=tg_id)

        user = await self.user_service.create_user(user_create=user)
        flag_verify = not verified and tg_id is not None

        if flag_verify:
            await self.auth_code.delete("login", code)
            await self.user_service.update_item(user.id, is_verified=True)
            await tgv_service.create_item(user_id=user.id, tg_id=tg_id)

        tokens = TokenCreator(user.id)

        return TgLoginAnswer(
            access=tokens.access,
            refresh=tokens.refresh,
            success_verify=flag_verify
        )

    async def login(self, code: str) -> LoginTokens | TgAuthCode:
        tg_id = await self.auth_code.get_id("login", code)

        if not tg_id:
            raise AuthError("истекший или несуществующий код")

        user = await self.user_service.get_user_by_tg_id(tg_id)

        if user:
            await self.auth_code.delete("login", code)
            return _create_auth_tokens(user.id)

        return TgAuthCode(code=code)

    async def verify(
            self, code: str,
            tg_id: int,
    ):
        tgv_service = TgVerifiedService(self.session)

        tg_verified = await tgv_service.repository.get_one_by(tg_id=tg_id)

        if tg_verified:
            return {"status": False, "msg": "Вы уже верифицировали аккаунт через Telegram"}

        user_id = await self.auth_code.get_id("verify", code)

        if not user_id:
            return {"status": False, "msg": "Код устарел или недействителен, попробуйте еще раз!"}

        if isinstance(user_id, bytes):
            user_id = int(user_id)

        user = await self.user_service.get_user_by_id(user_id)

        await tgv_service.create_item(tg_id=tg_id, user_id=user.id)
        await self.user_service.update_item(user.id, is_verified=True)
        await self.auth_code.delete("verify", code)

        return {"status": True, "msg": "Аккаунт успешно верифицирован!"}

    async def reset_password(self,  password: str, code: str):
        user_id = await self.auth_code.get_id("forget_password", code)

        if user_id is None:
            raise AuthError("Истекший код!")

        await self.user_service.get_by_or_raise(id=user_id)

        ensure_correct_password(password)
        password = generate_hashed_password(password)

        await self.user_service.update_item(user_id, password=password)
        await self.auth_code.delete("forget_password", code)

        return {"status": True, "msg": "Пароль успешно обновлен"}


class AuthLogic:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_service = UserService(session=session)
        self.auth_code = AuthCode(cache)



    async def login(self, creds: AuthCreds) -> LoginTokens:


        user = await self.user_service.get_by_or_raise(username=creds.username)

        if not verify_password(creds.password, user.password):

            raise InvalidPasswordError()

        return _create_auth_tokens(user.id)


    async def register(self, user_create: UserCreate) -> LoginTokens:
        ensure_correct_password(user_create.password)

        user = await self.user_service.create_user(user_create=user_create)
        c = ContainerService(self.session)

        await c.create_item(
            author_id=user.id, type=ContainerType.wall, title=f"user[{user.id}]-wall"
        )
        return _create_auth_tokens(user.id)

    async def change_password(self, user: User, pwd: PasswordChange):
        ensure_correct_password(pwd.new_password)

        if not verify_password(pwd.old_password, user.password):
            raise InvalidPasswordError()

        password = generate_hashed_password(pwd.new_password)

        await self.user_service.update_item(user.id, password=password)

    async def forget_password(self, username: str):
        user = await self.user_service.get_user_by_username(username)
        code = await self.auth_code.create( "forget_password", user.id)
        tg_ver = TgVerifiedService(self.session)
        tg_id = await tg_ver.get_by_or_raise(user_id=user.id)

        await broker.publish({
            "code": code, "tg_id": tg_id.tg_id},
        "forget-password"
        )




















