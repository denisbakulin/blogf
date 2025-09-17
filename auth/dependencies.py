from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from user.models import User
from auth.utils import decode_token, TokenTypes

from user.dependencies import get_user_service
from user.service import UserService

from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_session
from auth.service import AuthService
from auth.schemas import TokenInfo
from typing import Annotated

from core.exceptions import InvalidTokenError

security = HTTPBearer()


banned_token_types = [
    TokenTypes.change_email,
    TokenTypes.verify,
    TokenTypes.refresh
]

async def get_user_token(
        creds: HTTPAuthorizationCredentials = Depends(security),
) -> TokenInfo:
    if creds.scheme != "Bearer":
        raise InvalidTokenError(
            f"Invalid auth schema: {creds.scheme} (Bearer need)"
        )
    token = creds.credentials

    return decode_token(token)


async def get_current_user(
    token: TokenInfo = Depends(get_user_token),
    user_service: UserService = Depends(get_user_service)
) -> User:
    if token.type in banned_token_types:
        raise InvalidTokenError("Неверный тип токена")
    return await user_service.get_user_by_id(token.user_id)



async def get_verified_user(
    user: User = Depends(get_current_user),
) -> User:
    if not user.is_verified:
        return user
    raise HTTPException(401, "Почта не подтверждена")

async def get_admin(
    user: User = Depends(get_current_user),
) -> User:
    if user.is_admin:
        return user
    raise HTTPException(403, "Почта не подтверждена")


async def get_auth_service(
        session: AsyncSession = Depends(get_session)
) -> AuthService:
    return AuthService(session=session)


adminDep = Annotated[User, Depends(get_admin)]
verifiedUserDep = Annotated[User, Depends(get_verified_user)]
currentUserDep = Annotated[User, Depends(get_current_user)]
authServiceDep = Annotated[AuthService, Depends(get_auth_service)]