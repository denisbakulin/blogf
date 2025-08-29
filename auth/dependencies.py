from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException
from user.models import User
from auth.utils import decode_token
from auth.exceptions import InvalidTokenErr
from user.dependencies import get_user_service
from user.service import UserService
from user.exceptions import UserInactiveErr, UserNotFoundErr, UserNotVerifiedErr
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_session
from auth.service import AuthService
from auth.schemas import TokenInfo

security = HTTPBearer()


async def get_user_token(
        creds: HTTPAuthorizationCredentials = Depends(security),
) -> TokenInfo:
    if creds.scheme != "Bearer":
        raise HTTPException(
            401,
            f"Invalid auth schema: {creds.scheme} (Bearer need)"
        )
    token = creds.credentials
    try:
        decoded_token = decode_token(token)
    except InvalidTokenErr as e:
        raise HTTPException(401, detail=str(e))

    return decoded_token

async def get_current_user(
    token: TokenInfo = Depends(get_user_token),
    user_service: UserService = Depends(get_user_service)
) -> User:
    try:
        user = await user_service.get_user_by_id(token.user_id)
        return user
    except UserInactiveErr as e:
        raise HTTPException(403, detail=str(e))
    except UserNotFoundErr as e:
        raise HTTPException(404, detail=str(e))


async def get_verified_user(
    user: User = Depends(get_user_token),
) -> User:
    if user.is_verified:
        return user
    raise HTTPException(401, "Почта не подтверждена")


async def get_auth_service(
        session: AsyncSession = Depends(get_session)
) -> AuthService:
    return AuthService(session=session)
