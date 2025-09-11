from user.repository import UserRepository
from user.schemas import UserCreate, UserUpdate
from user.models import User
from user.exceptions import UserAlreadyExistErr, UserNotFoundErr, UserInactiveErr, IncorrectPasswordErr
from user.utils import verify_password, generate_hashed_password
from sqlalchemy.ext.asyncio import AsyncSession


from admin.schemas import AdminUserCreate, AdminUserUpdate


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UserRepository(session)

    async def create_user(self, user_data: UserCreate | AdminUserCreate) -> User:

        existing_username = await self.repo.get_user(username=user_data.username)

        if existing_username:
            raise UserAlreadyExistErr(f"Пользователь с username={user_data.username} уже существует!")

        existing_email = await self.repo.get_user(email=user_data.email)

        if existing_email:
            raise UserAlreadyExistErr(f"Пользователь с указанной почтой уже существует!")

        hashed_password = generate_hashed_password(password=user_data.password)

        user_data.password = hashed_password

        user = self.repo.create_user(
            user_data.model_dump(),
        )

        await self.update_user(user, UserUpdate(bio=user_data.bio, avatar=user_data.avatar))

        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def _get_user_by(self, **filter) -> User:
        user = await self.repo.get_user(**filter)

        if not user:
            raise UserNotFoundErr(f"Пользователь не найден!")

        return user

    async def get_user_by_id(self, user_id: int) -> User:
        return await self._get_user_by(id=user_id)

    async def get_user_by_username(self, username: str) -> User:
        return await self._get_user_by(username=username)



    async def create_admin(self):

        admin = await self.repo.user_exists(is_admin=True)

        if admin: return

        hashed_password = generate_hashed_password(password="admin")

        admin_data = {
            "username": "admin",
            "password": hashed_password,
            "is_admin": True,
            "is_verified": True,
            "email": "dtorkon@yandex.ru",
        }

        admin = self.repo.create_user(admin_data)

        await self.session.commit()
        await self.session.refresh(admin)

        return admin


    async def update_user(self, user: User, update_info: UserUpdate | AdminUserUpdate ) -> User:
        if update_info.username:

            existing = await self.repo.get_user(username=update_info.username)

            if existing:
                raise UserAlreadyExistErr(f"Пользователь с username={update_info.username} уже существует!")

        if update_info.bio:
            update_info.bio = update_info.bio[:2000]

        updated_user = await self.repo.update_user_info(user, update_info.model_dump(exclude_none=True))

        await self.session.commit()
        await self.session.refresh(updated_user)

        return updated_user

    async def update_important_user_info(self, user: User, **update_info) -> User:
        return await self.repo.update_user_info(user, **update_info)


    async def change_password(self, user: User, old_password, new_password) -> User:
        if not verify_password(old_password, user.password):
            raise IncorrectPasswordErr("Пароль указан не верно!")

        password = generate_hashed_password(new_password)


        await self.repo.update_user_info(user, {"password":password})

        await self.session.commit()
        await self.session.refresh(user)


    async def change_email(self, user: User, email: str):
        existing_email = await self.repo.get_user(email=email)

        if existing_email:
            raise UserAlreadyExistErr("Пользователь с указанной почтой уже существует!")

        await self.repo.update_user_info(user, {"email":email, "is_verified":False})
        await self.session.commit()
        await self.session.refresh(user)



    async def search_users(self, username: str, offset: int, limit: int) -> list[User]:
        users = await self.repo.search_users(username, offset, limit)
        if not users:
            raise UserNotFoundErr("Пользователи не найдены")
        return users





