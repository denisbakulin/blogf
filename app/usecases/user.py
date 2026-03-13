from entities.user import Settings, User
from schemas.user import (
    UserProfile,
    UserProfileShow,
    UserSettings,
    UserShow,
    UserUpdate,
)
from services.user import UserService


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


    async def get_settings(self, user: User) -> Settings:
        return await self.user_service.settings_service.get_by_or_raise(user_id=user.id)

    async def update_settings(self, user: User, update: UserSettings) -> Settings:
        return await self.user_service.update_user_settings(user=user, update=update)




