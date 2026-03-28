from typing import Annotated

from base.db import getSessionDep
from fastapi import Depends
from services.user import UserService


def get_user_service(
        session: getSessionDep
) -> UserService:
    return UserService(session=session)


userServiceDep = Annotated[UserService, Depends(get_user_service)]

