from typing import Annotated

from auth.base import BaseAuth
from auth.google import GoogleAuth
from auth.telegram import TelegramAuth
from base.db import get_session
from deps.user import userServiceDep
from entities.user import User
from exceptions.auth import InvalidTokenError
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from schemas.auth import TokenInfo
from sqlalchemy.ext.asyncio import AsyncSession
from utils.auth import get_decoded_token

security = HTTPBearer()
optional_security = HTTPBearer(auto_error=False)


def decode_token_from_creds(creds: HTTPAuthorizationCredentials) -> TokenInfo:
    if creds.scheme != "Bearer":
        raise InvalidTokenError(
            f"Invalid auth schema: {creds.scheme} (Bearer need)"
        )
    token = creds.credentials

    return get_decoded_token(token)

async def get_user_token(
        creds: HTTPAuthorizationCredentials = Depends(security),
) -> TokenInfo:
    return decode_token_from_creds(creds)


async def get_current_user(
    user_service: userServiceDep,
    token: TokenInfo = Depends(get_user_token),
) -> User:
    return await user_service.get_user_by_id(token.user_id)



async def get_base_auth(
        session: AsyncSession = Depends(get_session)
) -> BaseAuth:
    return BaseAuth(session=session)

async def get_tg_auth(
        session: AsyncSession = Depends(get_session)
) -> TelegramAuth:
    return TelegramAuth(session)

async def get_google_auth(
        session: AsyncSession = Depends(get_session)
) -> GoogleAuth:
    return GoogleAuth(session)



currentUserDep = Annotated[User, Depends(get_current_user)]

baseAuthServiceDep = Annotated[BaseAuth, Depends(get_base_auth)]
tgAuthServiceDep = Annotated[TelegramAuth, Depends(get_tg_auth)]
googleAuthServiceDep = Annotated[GoogleAuth, Depends(get_google_auth)]
