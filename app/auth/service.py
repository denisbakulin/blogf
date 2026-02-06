from sqlalchemy.ext.asyncio import AsyncSession

from auth.exceptions import InvalidPasswordError
from auth.schemas import AuthCreds, LoginTokens
from auth.utils import TokenCreator, generate_8char_code
from user.schemas import UserCreate
from user.service import UserService
from user.utils import verify_password
from fastapi_cache import FastAPICache



class AuthService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_service = UserService(session=session)
        self.cache_backand = FastAPICache.get_backend()


    async def login(self, creds: AuthCreds) -> LoginTokens:
        user = await self.user_service.get_user_by_username(creds.username)

        if not verify_password(creds.password, user.password):

            raise InvalidPasswordError()

        return self._create_auth_tokens(user.id)

    async def register(self, user_create: UserCreate) -> LoginTokens:
        user = await self.user_service.create_user(user_create=user_create)

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

















