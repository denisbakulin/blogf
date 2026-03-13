from base.exceptions import EntityAlreadyExists
from base.service import BaseService
from entities.user import Profile, Settings, User
from helpers.search import Pagination
from repositories.user import ProfileRepository, SettingsRepository, UserRepository
from schemas.user import UserSettings, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from utils.user import UserSearchParams, ensure_correct_username


class ProfileService(BaseService[Profile, ProfileRepository]):
    def __init__(self, session: AsyncSession):
        super().__init__(Profile, session, ProfileRepository)


class SettingsService(BaseService[Settings, SettingsRepository]):
    def __init__(self, session: AsyncSession):
        super().__init__(Settings, session, SettingsRepository)


class UserService(BaseService[User, UserRepository]):
    # сделать нормальную обработку username

    def __init__(self, session: AsyncSession):
        super().__init__(User, session, UserRepository)
        self.profile_service = ProfileService(session)
        self.settings_service = SettingsService(session)


    async def get_user_profile(self, user: User) -> Profile:
        return await self.profile_service.get_by_or_raise(user_id=user.id)



    async def create_user(self, name: str, username: str) -> User:
        ensure_correct_username(username)
        await self.check_already_exists(username=username)


        user = await self.create_item(
            name=name, username=username
        )

        await self.profile_service.create_item(user_id=user.id)
        await self.settings_service.create_item(user_id=user.id)

        return user


    async def get_user_by_id(self, user_id: int) -> User:
        return await self.get_item_by_id(user_id)


    async def get_user_by_username(self, username: str) -> User:
        return await self.get_by_or_raise(username=username)



    async def update_user(self, user: User, update: UserUpdate) -> User:
        username = ensure_correct_username(update.username) if update.username else None
        upd_user = await self.repository.get_one_by(username=username)

        if upd_user and upd_user.id != user.id:
            raise EntityAlreadyExists(entity="user", username=username)

        update.username = username

        user_data = update.model_dump(exclude_none=True)
        profile_data: dict | None = user_data.pop("profile", None)

        await self.update_item(user.id, **user_data)

        if profile_data is not None:

            profile = await self.profile_service.repository.get_one_by(user_id=user.id)

            await self.profile_service.update_item(
                profile.id, **profile_data
            )

        return user



    async def search_users(self, search: UserSearchParams, pagination: Pagination) -> list[User]:
        return await self.repository.search(
            field=search.field, value=search.value, strict=search.strict,  **pagination.dict()
        )

    async def update_user_settings(self, user: User, update: UserSettings) -> Settings:
        settings = await self.settings_service.repository.get_one_by(user_id=user.id)

        settings = await self.settings_service.update_item(
            settings.id, **update.model_dump(exclude_none=True)
        )

        return settings


    async def get_user_by_tg_id(self, tg_id: int) -> User | None:
        return await self.repository.get_user_by_tg_id(tg_id)






