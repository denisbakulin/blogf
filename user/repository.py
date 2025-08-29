from user.models import User, Profile
from base.repository import BaseRepository
from sqlalchemy import select
from typing import Optional


class UserRepository(BaseRepository):

    def create_user(self, user_data: dict) -> User:
        user = User(**user_data)
        profile = Profile()
        user.profile = profile
        self.session.add(user)
        return user

    async def get_user(
            self,
            user_id: Optional[int] = None,
            username: Optional[str] = None,
            email: Optional[str] = None
    ) -> Optional[User]:
        stmt = select(User)

        if user_id:
            stmt = stmt.where(User.id == user_id)
        elif username:
            stmt = stmt.where(User.username == username)
        elif email:
            stmt = stmt.where(User.email == email)
        else:
            return

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    @staticmethod
    def _update_field(user, field, value):
        {
            field in {"username", "email"}: lambda: setattr(user, field, value),
            field in {"avatar", "bio"}: lambda: setattr(user.profile, field, value),
        }.get(True, lambda: 0)()

    async def update_user_info(self, user: User, updates: dict) -> User:
        for key, value in updates.items():
            self._update_field(user, key, value)

        return user

    async def update_user_password(self, user: User, password):
        user.password = password

    async def deactivate_user(self, user: User):
        user.is_active = False

    async def activate_user(self, user: User):
        user.is_active = True

    async def verify_user(self, user: User):
        user.is_verified = True

    async def search_users(self, username: str, offset: int, limit: int) -> list[User]:
        stmt = (select(User)
                .where(User.username
                       .ilike(f"%{username}%"))
                .offset(offset)
                .limit(limit)
        )

        result = await self.session.execute(stmt)

        users = result.scalars().all()

        return list(users)



