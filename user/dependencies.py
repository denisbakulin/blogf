from user.repository import UserRepository
from user.service import UserService
from core.db import get_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


def get_user_repo(session: AsyncSession):
    return UserRepository(session=session)


def get_user_service(
        session: AsyncSession = Depends(get_session)
) -> UserService:
    return UserService(session=session)

