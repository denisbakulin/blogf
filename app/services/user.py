from base.exceptions import EntityAlreadyExists
from base.service import BaseService
from exceptions.auth import InvalidPasswordError
from helpers.search import Pagination
from models.user import Profile, Settings, User
from repositories.user import UserRepository, ProfileRepository, SettingsRepository
from schemas.user import PasswordChange, UserCreate, UserSettings, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from utils.user import (UserSearchParams, generate_hashed_password,
                        verify_password)

from DTO.user import UserDTO, UserCreds, SettingsDTO, ProfileDTO, UserProfileDTO, UserSettingsDTO

class ProfileService(BaseService[Profile, ProfileRepository, ProfileDTO]):
    def __init__(self, session: AsyncSession):
        super().__init__(Profile, session, ProfileRepository)


class SettingsService(BaseService[Settings, SettingsRepository, SettingsDTO]):
    def __init__(self, session: AsyncSession):
        super().__init__(Settings, session, SettingsRepository)


class UserService(BaseService[User, UserRepository, UserDTO]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session, UserRepository)
        self.profile_service = ProfileService(session)
        self.settings_service = SettingsService(session)


    async def get_user_profile(self, user: UserDTO) -> UserProfileDTO:
        profile = await self.profile_service.get_by_or_raise(user_id=user.id)

        return UserProfileDTO(user=user, profile=profile)



    async def create_user(self, user_create: UserCreate) -> UserDTO:
        await self.check_already_exists(username=user_create.username)

        hashed_password = generate_hashed_password(password=user_create.password)

        user_create.username = user_create.username.lower()
        user_create.password = hashed_password

        user = await self.create_item(
            **user_create.model_dump(),
        )
        await self.profile_service.create_item(user_id=user.id)
        await self.settings_service.create_item(user_id=user.id)

        return user


    async def get_user_by_id(self, user_id: int) -> UserDTO:
        return await self.get_item_by_id(user_id)


    async def get_user_by_username(self, username: str) -> UserDTO:
        return await self.get_by_or_raise(username=username)

    async def get_user_creds_by_username(self, username: str) -> UserCreds:
        await self.get_user_by_username(username)
        return await self.repository.get_user_creds_by_username(username)


    async def update_user(self, user: UserDTO, update: UserUpdate) -> UserDTO:
        upd_user = await self.repository.get_one_by(username=update.username)

        if upd_user and upd_user.username != user.username:
            raise EntityAlreadyExists(entity="user", username=update.username)

        user_data = update.model_dump(exclude_none=True)
        profile_data: dict | None = user_data.pop("profile", None)

        await self.update_item(user.id, **user_data)

        if profile_data is not None:

            profile = await self.profile_service.repository.get_orm(user_id=user.id)

            await self.profile_service.update_item(
                profile.id, **profile_data
            )

        return user


    async def change_password(self, user: UserDTO, pwd: PasswordChange):
        user_creds = await self.get_user_creds_by_username(user.username)

        if not verify_password(pwd.old_password, user_creds.password):
            raise InvalidPasswordError()

        password = generate_hashed_password(pwd.new_password)

        await self.update_item(user.id, password=password)


    async def search_users(self, search: UserSearchParams, pagination: Pagination) -> list[UserDTO]:
        return await self.repository.search(
            field=search.field, value=search.value, strict=search.strict,  **pagination.dict()
        )

    async def update_user_settings(self, user: UserDTO, update: UserSettings) -> SettingsDTO:
        settings = await self.settings_service.repository.get_orm(user_id=user.id)

        settings = await self.settings_service.update_item(
            settings.id, **update.model_dump(exclude_none=True)
        )

        return settings








