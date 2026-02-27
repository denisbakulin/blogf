from typing import Annotated

from base.db import get_session
from base.exceptions import EntityLockedError
from exceptions.auth import InvalidTokenError
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from schemas.auth import TokenInfo
from logic.auth import AuthLogic
from models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from deps.user import userServiceDep
from utils.auth import decode_token
from DTO.user import UserDTO

security = HTTPBearer()
optional_security = HTTPBearer(auto_error=False)


def decode_token_from_creds(creds: HTTPAuthorizationCredentials) -> TokenInfo:
    if creds.scheme != "Bearer":
        raise InvalidTokenError(
            f"Invalid auth schema: {creds.scheme} (Bearer need)"
        )
    token = creds.credentials

    return decode_token(token)

async def get_user_token(
        creds: HTTPAuthorizationCredentials = Depends(security),
) -> TokenInfo:
    return decode_token_from_creds(creds)


async def get_current_user(
    user_service: userServiceDep,
    token: TokenInfo = Depends(get_user_token),
) -> UserDTO:

    user = await user_service.get_user_by_id(token.user_id)

    if user.is_active:
        return user

    raise EntityLockedError(
        message=f"Пользователь {user.username} временно заблокирован"
    )


async def get_auth_logic(
        session: AsyncSession = Depends(get_session)
) -> AuthLogic:
    return AuthLogic(session=session)


currentUserDep = Annotated[UserDTO, Depends(get_current_user)]
authServiceDep = Annotated[AuthLogic, Depends(get_auth_logic)]