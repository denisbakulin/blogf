from operator import ge
from typing import Annotated, Callable

from auth.exceptions import InvalidTokenError
from auth.schemas import TokenInfo
from auth.service import AuthService
from auth.utils import decode_token
from base.db import get_session
from base.exceptions import EntityLockedError
from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from user.deps import get_user_service
from user.model import User, UserRoleEnum
from user.service import UserService


Operator = Callable[[UserRoleEnum, UserRoleEnum], bool]

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


async def get_anon(
        user_service: UserService = Depends(get_user_service)
) -> User:
    return await user_service.get_anonymous()


anonDep = Annotated[User, Depends(get_anon)]

async def get_current_user(
    token: TokenInfo = Depends(get_user_token),
    user_service: UserService = Depends(get_user_service)
) -> User:
    user = await user_service.get_user_by_id(token.user_id)

    if user.is_active:
        return user

    raise EntityLockedError(
        message=f"Пользователь {user.username} временно заблокирован"
    )



def role_validate(role: UserRoleEnum, operator: Operator = ge):
    """Проверяет права пользователя"""

    async def wrapper(user: User = Depends(get_current_user)):
        if operator(user.role, role):
            return user
        raise HTTPException(detail="Недостаточно прав", status_code=403)
    return wrapper


async def get_auth_service(
        session: AsyncSession = Depends(get_session)
) -> AuthService:
    return AuthService(session=session)



async def get_anon_or_current_user(
        creds: HTTPAuthorizationCredentials | None = Depends(optional_security),
        user_service: UserService = Depends(get_user_service)
):
    if creds is None:
        return await user_service.get_anonymous()
    try:
        user_id = decode_token_from_creds(creds).user_id
        return await user_service.get_user_by_id(user_id)
    except InvalidTokenError:
        return await user_service.get_anonymous()


getCurrentOrAnonUser = Annotated[User, Depends(get_anon_or_current_user)]
currentUserDep = Annotated[User, Depends(get_current_user)]
authServiceDep = Annotated[AuthService, Depends(get_auth_service)]