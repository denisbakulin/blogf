from exceptions.auth import InvalidPasswordError
from fastapi_cache import FastAPICache
from schemas.auth import AuthCreds, LoginTokens
from services.user import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate
from utils.auth import TokenCreator, generate_8char_code
from utils.user import verify_password
# from models.container import ContainerType
# from services.container import ContainerService


from deps.tg_verified import TgVerifiedService

class AuthLogic:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_service = UserService(session=session)
        # self.container_service = ContainerService(session)
        self.cache_backand = FastAPICache.get_backend()



    async def login(self, creds: AuthCreds) -> LoginTokens:

        user = await self.user_service.get_by_or_raise(username=creds.username)

        if not verify_password(creds.password, user.password):

            raise InvalidPasswordError()

        return self._create_auth_tokens(user.id)


    async def register(self, user_create: UserCreate) -> LoginTokens:
        user = await self.user_service.create_user(user_create=user_create)
        # wall = await self.container_service.create_item(
        #     author_id=user.id, type=ContainerType.wall
        # )
        return self._create_auth_tokens(user.id)


    def _create_auth_tokens(self, user_id: int) -> LoginTokens:
        tokens = TokenCreator(user_id)

        return LoginTokens(
            access=tokens.access,
            refresh=tokens.refresh
        )

    async def create_verify_code(self, user_id: int):
        code = generate_8char_code()
        await self.cache_backand.set(code, user_id, expire=600)
        return code

    async def check_verify_code(self, code):
        return  await self.cache_backand.get(code)


    async def bot_verify(
            self, code: str,
            tg_id: int,
            tgv_service: TgVerifiedService
    ):
        tg_verified = await tgv_service.repository.get_one_by(tg_id=tg_id)

        if tg_verified:
            return {"status": False, "msg": "Вы уже верифицировали аккаунт через Telegram"}

        user_id = await self.check_verify_code(code)

        if not user_id:
            return {"status": False, "msg": "Код устарел или недействителен, попробуйте еще раз!"}

        if isinstance(user_id, bytes):
            user_id = user_id.decode("utf-8")

        user = await self.user_service.get_user_by_id(int(user_id))

        await tgv_service.create_item(tg_id=tg_id)
        await self.user_service.update_item(user.id, is_verified=True)
        await self.cache_backand.set(code, 1, expire=1)

        return {"status": True, "msg": "Аккаунт успешно верифицирован!"}
















