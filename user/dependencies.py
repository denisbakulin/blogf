from user.service import UserService
from core.db import get_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

def get_user_service(
        session: AsyncSession = Depends(get_session)
) -> UserService:
    return UserService(session=session)


userServiceDep = Annotated[UserService, Depends(get_user_service)]