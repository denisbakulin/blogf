from sqlalchemy.ext.asyncio import AsyncSession
from user.service import UserService

from user.schemas import UserCreate
from auth.utils import create_access_token, create_refresh_token, create_verify_token, decode_token
from auth.schemas import Tokens, AuthCreds
from user.utils import verify_password
from auth.exceptions import InvalidPasswordErr, InvalidTokenErr
from user.models import User



class AuthService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_service = UserService(session=session)

    async def register(self, user_info: UserCreate) -> list[str]:
        user = await self.user_service.create_user(user_info=user_info)
        tokens = [create_verify_token(user.id), create_access_token(user.id)]
        return tokens


    async def login(self, creds: AuthCreds) -> Tokens | None:
        user = await self.user_service.get_user_by_username(creds.username)

        if not verify_password(creds.password, user.password):
            raise InvalidPasswordErr("Пароль не правильный!")

        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        return Tokens(access_token=access_token, refresh_token=refresh_token)

    async def verificate_user(self, token: str) -> Tokens:
        token = decode_token(token)
        if token.type != "access":
            raise InvalidTokenErr("Не access токен")

        user = await self.user_service.get_user_by_id(token.user_id)

        await self.session.commit()
        await self.session.refresh(user)

        access_token = create_access_token(token.user_id)
        refresh_token = create_refresh_token(token.user_id)

        return Tokens(access_token=access_token, refresh_token=refresh_token)







