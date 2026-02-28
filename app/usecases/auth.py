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

class AuthLogic:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_service = UserService(session=session)
        # self.container_service = ContainerService(session)
        self.cache_backand = FastAPICache.get_backend()



    async def login(self, creds: AuthCreds) -> LoginTokens:

        user_creds = await self.user_service.get_user_creds_by_username(creds.username)

        if not verify_password(creds.password, user_creds.password):

            raise InvalidPasswordError()

        return self._create_auth_tokens(user_creds.id)


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
        user_id = await self.cache_backand.get(code)
        return user_id

















