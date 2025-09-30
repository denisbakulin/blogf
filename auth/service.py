from sqlalchemy.ext.asyncio import AsyncSession
from user.service import UserService

from user.schemas import UserCreate
from auth.utils import TokenCreator, decode_token,TokenTypes
from auth.schemas import LoginTokens, AuthCreds
from user.utils import verify_password
from auth.exceptions import InvalidPasswordError, InvalidTokenError



class AuthService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_service = UserService(session=session)


    async def register(self, user_info: UserCreate) -> list[str]:
        user = await self.user_service.create_user(user_data=user_info)
        tokens = TokenCreator(user.id)
        return [tokens.pending_access, tokens.verify]


    async def login(self, creds: AuthCreds) -> LoginTokens | None:
        user = await self.user_service.get_user_by_username(creds.username)

        if not verify_password(creds.password, user.password):
            raise InvalidPasswordError

        tokens = TokenCreator(user.id)

        return LoginTokens(access_token=tokens.access, refresh_token=tokens.refresh)

    async def _verify_user(self, token: str, target_type: TokenTypes) -> LoginTokens:
        token = decode_token(token)

        if token.type != target_type:
            raise InvalidTokenError(f"Не валидный токен для верификации {token.type} {target_type}")

        user = await self.user_service.get_user_by_id(token.user_id)

        await self.user_service.update_important_user_info(user, is_verified=True)
        await self.session.commit()

        tokens = TokenCreator(user.id)

        return LoginTokens(access_token=tokens.access, refresh_token=tokens.refresh)

    async def verify_user_by_email(self, token: str) -> LoginTokens:
        return await self._verify_user(token, TokenTypes.verify)


    async def verify_new_user_email(self, token: str):
        return await self._verify_user(token, TokenTypes.change_email)





