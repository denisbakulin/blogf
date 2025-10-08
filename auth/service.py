from sqlalchemy.ext.asyncio import AsyncSession

from auth.exceptions import InvalidPasswordError, InvalidTokenError
from auth.schemas import AuthCreds, LoginTokens
from auth.utils import TokenCreator, TokenTypes, decode_token
from user.schemas import UserCreate
from user.service import UserService
from user.utils import verify_password
from core.service import BaseService
from auth.model import UsedToken

from auth.utils import TokenTypes



class AuthService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_service = UserService(session=session)
        self.token_service = BaseService[UsedToken, session](UsedToken, session)



    async def register(self, user_info: UserCreate) -> list[str]:
        user = await self.user_service.create_user(user_data=user_info)

        tokens = TokenCreator(user.id)
        return [tokens.pending_access, tokens.verify]


    async def login(self, creds: AuthCreds) -> LoginTokens:
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

        await self.user_service.update_item(user, is_verified=True)

        await self.token_service.create_item(token=token, type=target_type)

        tokens = TokenCreator(user.id)

        return LoginTokens(access_token=tokens.access, refresh_token=tokens.refresh)

    async def verify_by_email(self, token: str) -> LoginTokens:
        await self.token_service.check_already_exists(token=token, type=TokenTypes.verify)

        return await self._verify_user(token, TokenTypes.verify)


    async def change_email(self, token: str):
        await self.token_service.check_already_exists(token=token, type=TokenTypes.change_email)

        return await self._verify_user(token, TokenTypes.change_email)







