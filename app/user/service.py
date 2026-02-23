from auth.exceptions import InvalidPasswordError
from base.exceptions import EntityAlreadyExists
from base.service import BaseService
from helpers.search import Pagination
from sqlalchemy.ext.asyncio import AsyncSession
from user.model import Profile, Settings, User, UserRoleEnum
from user.repository import UserRepository
from user.schemas import PasswordChange, UserCreate, UserSettings, UserUpdate
from user.utils import (UserSearchParams, generate_hashed_password,
                        verify_password)


class UserService(BaseService[User, UserRepository]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session, UserRepository)
        self.profile_service = BaseService(Profile, session)



    async def create_user(self, user_create: UserCreate) -> User:
        await self.check_already_exists(username=user_create.username)

        hashed_password = generate_hashed_password(password=user_create.password)

        user_create.password = hashed_password

        user = self.repository.create(
            **user_create.model_dump(),
        )


        return user


    async def create_super_admin(self, admin_data: UserCreate) -> User | None:
        admin = await self.repository.get_one_by(role=UserRoleEnum.SUPER_ADMIN)

        if admin:
            return admin

        admin = await self.create_user(user_create=admin_data)

        return await self.update_item(admin, role=UserRoleEnum.SUPER_ADMIN)

    async def create_anon(self, anon_data: UserCreate) -> User:

        anon = await self.repository.get_one_by(role=UserRoleEnum.ANONYMOUS)

        if anon:
            return anon

        anon = await self.create_user(user_create=anon_data)

        return await self.update_item(anon, role=UserRoleEnum.ANONYMOUS)

    async def get_anonymous(self) -> User:
        return await self.get_item_by(role=UserRoleEnum.ANONYMOUS)

    async def get_user_by_id(self, user_id: int) -> User:
        return await self.get_item_by_id(user_id)


    async def get_user_by_username(self, username: str) -> User:
        return await self.get_item_by(username=username)


    async def update_user(self, user: User, user_update: UserUpdate) -> User:
        upd_user = await self.repository.get_one_by(username=user_update.username)

        if upd_user and upd_user.username != user.username:
            raise EntityAlreadyExists(entity="user", username=user_update.username)

        user_data = user_update.model_dump(exclude_none=True)
        profile_data: dict | None = user_data.pop("profile", None)

        await self.update_item(user, **user_data)


        if profile_data is not None:
            await self.profile_service.update_item(
                user.profile, **profile_data
            )
        return user




    async def change_password(self, user: User, pwd: PasswordChange):
        if not verify_password(pwd.old_password, user.password):
            raise InvalidPasswordError()

        password = generate_hashed_password(pwd.new_password)

        await self.update_item(user, password=password)

    async def search_users(self, search: UserSearchParams, pagination: Pagination) -> list[User]:
        return await self.search_items(
            search, pagination,
            inner_props={
                "settings.show_in_search": True
            }
        )

    async def edit_user_settings(self, user: User, settings: UserSettings) -> Settings:

        await self.update_item(user.settings, **settings.dict())

        return user.settings








