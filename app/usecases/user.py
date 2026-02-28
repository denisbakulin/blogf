from entities.user import User
from schemas.user import UserUpdate
from DTO.user import  UserDTO
from schemas.user import UserProfileShow, UserProfile, UserShow, UserSettings

from services.user import UserService

from dataclasses import asdict
from utils.user import UserSearchParams
from typing import Any
from helpers.search import Pagination

class UserLogic:

    def __init__(
            self,
            user_service: UserService
    ):
        self.user_service = user_service

    async def get_profile(self, user: UserDTO) -> UserProfileShow:

        res = await self.user_service.get_user_profile(user)

        profile = UserProfile(**asdict(res.profile))
        user = UserShow(**asdict(res.user))

        return UserProfileShow(user=user, profile=profile)

    async def update(self, user: UserDTO, update: UserUpdate) -> UserProfileShow:
        user = await self.user_service.update_user(user=user, update=update)

        return await self.get_profile(user)


    async def get_settings(self, user: UserDTO) -> UserSettings:
        settings = await self.user_service.settings_service.get_by_or_raise(user_id=user.id)

        return UserSettings(**asdict(settings))

    async def update_settings(self, user: UserDTO, update: UserSettings) -> UserSettings:
        settings = await self.user_service.update_user_settings(user=user, update=update)

        return UserSettings(**asdict(settings))

    async def search(self, search: UserSearchParams, pagination: Pagination) -> list[UserShow]:
        res = await self.user_service.search_users(
            search=search, pagination=pagination,
        )
        print(res, search, pagination)
        return list(UserShow(**asdict(user)) for user in res)
