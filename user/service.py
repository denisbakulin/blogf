from user.repository import UserRepository
from user.schemas import UserCreate, UserUpdate, PasswordChange
from user.models import User
from user.exceptions import UserAlreadyExistErr, UserNotFoundErr, UserInactiveErr, IncorrectPasswordErr
from user.utils import verify_password, generate_hashed_password
from sqlalchemy.ext.asyncio import AsyncSession



class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = UserRepository(session)

    async def create_user(self, user_info: UserCreate) -> User:

        existing_username = await self.repo.get_user(username=user_info.username)

        if existing_username:
            raise UserAlreadyExistErr(f"Пользователь с username={user_info.username} уже существует!")

        existing_email = await self.repo.get_user(email=user_info.email)

        if existing_email:
            raise UserAlreadyExistErr(f"Пользователь с email={user_info.email} уже существует!")

        hashed_password = generate_hashed_password(password=user_info.password)
        user_info.password = hashed_password

        user = self.repo.create_user(user_info.model_dump())

        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def update_user(self, user: User, update_info: UserUpdate) -> User:
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

    async def change_password(self, user: User, old_password, new_password) -> User:
        if not verify_password(old_password, user.password):
            raise IncorrectPasswordErr("Пароль указан не верно!")

        password = generate_hashed_password(new_password)

        await self.repo.update_user_password(user, password)

        await self.session.commit()
        await self.session.refresh(user)

        return user


    async def get_user_by_id(self, user_id: int) -> User:
        user = await self.repo.get_user(user_id=user_id)

        if not user:
            raise UserNotFoundErr(f"Пользователь с id={user_id} не найден!")

        if not user.is_active:
            raise UserInactiveErr(f"Пользователь с id={user_id} деактивирован!")

        return user

    async def get_user_by_username(self, username: str) -> User:
        user = await self.repo.get_user(username=username)

        if not user:
            raise UserNotFoundErr(f"Пользователь с username={username} не найден!")

        if not user.is_active:
            raise UserInactiveErr(f"Пользователь с username={username} деактивирован!")

        return user


    async def get_user(self, identifier: str) -> User:
        if identifier.isdigit():
            return await self.get_user_by_id(int(identifier))
        elif identifier.startswith("@"):
            return await self.get_user_by_username(identifier[1:])
        raise UserNotFoundErr(f"Неверный параметр для поиска пользователя")


    async def search_users(self, username: str, offset: int, limit: int) -> list[User]:
        users = await self.repo.search_users(username, offset, limit)
        if not users:
            raise UserNotFoundErr("Пользователи не найдены")
        return users

    async def verify_user(self, user: User):
        await self.repo.verify_user(user)


