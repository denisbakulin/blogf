from typing import Annotated

from base.db import getSessionDep
from fastapi import Depends
from DTO.user import UserDTO
from services.user import UserService
from logic.user import UserLogic


def get_user_service(
        session: getSessionDep
) -> UserService:
    return UserService(session=session)


userServiceDep = Annotated[UserService, Depends(get_user_service)]


async def get_user(
        user_service: userServiceDep,
        username: str
) -> UserDTO:
    return await user_service.get_user_by_username(username)


async def get_user_logic(
        user_service: userServiceDep
) -> UserLogic:
    return UserLogic(user_service)


userLogicDep = Annotated[UserLogic, Depends(get_user_logic)]
userDep = Annotated[UserDTO, Depends(get_user)]

