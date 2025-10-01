from typing import Literal, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from core.repository import BaseRepository
from user.model import User

secure_fields = Literal["password", "is_active", "is_verify"]




class UserRepository(BaseRepository[User]):

    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    def create_user(self, **user_data) -> User:
        return self.create(**user_data)


    async def get_user(
            self,
            **filters
    ) -> Optional[User]:
        return await self.get_one_by(**filters)


    async def search_users(self, username: str, offset: int, limit: int) -> list[User]:
        return await self.search(
            "username",
            username,
            offset=offset,
            limit=limit
        )






