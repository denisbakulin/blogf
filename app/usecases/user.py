from entities.user import User
from schemas.user import UserUpdate

from schemas.user import UserProfileShow, UserProfile, UserShow, UserSettings

from services.user import UserService

from dataclasses import asdict
from utils.user import UserSearchParams

from helpers.search import Pagination

class UserLogic:

    def __init__(
            self,
            user_service: UserService
    ):
        self.user_service = user_service

    async def get_profile(self, user: User) -> UserProfileShow:

        profile = await self.user_service.get_user_profile(user)

        profile = UserProfile.from_orm(profile)
        user = UserShow.from_orm(user)

        return UserProfileShow(user=user, profile=profile)

    async def update(self, user: User, update: UserUpdate) -> UserProfileShow:
        user = await self.user_service.update_user(user=user, update=update)

        return await self.get_profile(user)


    async def get_settings(self, user: User) -> UserSettings:
        settings = await self.user_service.settings_service.get_by_or_raise(user_id=user.id)

        return UserSettings(**asdict(settings))

    async def update_settings(self, user: User, update: UserSettings) -> UserSettings:
        settings = await self.user_service.update_user_settings(user=user, update=update)

        return UserSettings.from_orm(settings)

    async def search(self, search: UserSearchParams, pagination: Pagination) -> list[UserShow]:
        res = await self.user_service.search_users(
            search=search, pagination=pagination,
        )
        print(res, search, pagination)
        return list(UserShow.from_orm(user) for user in res)
