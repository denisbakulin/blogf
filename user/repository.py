from user.models import User, Profile
from core.repository import BaseRepository
from sqlalchemy import select
from typing import Optional, Literal


secure_fields = Literal["password", "is_active", "is_verify"]




class UserRepository(BaseRepository):

    def create_user(self, user_data: dict) -> User:
        user = User(**user_data)
        self.session.add(user)
        return user

    async def get_user(
            self,
            **filters
    ) -> Optional[User]:

        stmt = select(User).filter_by(**filters)
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    @staticmethod
    def _update_field(user, field, value) -> None:
        {
            field in {"avatar", "bio"}: lambda: setattr(user.profile, field, value),
        }.get(True, lambda: setattr(user, field, value))()

    async def update_user_info(self, user: User, updates: dict) -> User:
        for key, value in updates.items():
            self._update_field(user, key, value)

        return user


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

    async def user_exists(
        self,
        ** filters
    ) -> bool:
        stmt = select(User).filter_by(**filters)
        result = await self.session.execute(stmt)

        user = result.first()

        return bool(user)






