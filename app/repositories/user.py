from base.repository import BaseRepository
from entities.user import User, Profile, Settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from typing import Any
from deps.tg_verified import TgVerified

class ProfileRepository(BaseRepository[Profile]):
    def __init__(self, session: AsyncSession):
        super().__init__(Profile, session)


class SettingsRepository(BaseRepository[Settings]):
    def __init__(self, session: AsyncSession):
        super().__init__(Settings, session)



class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)


    async def get_user_by_tg_id(self, tg_id: int) -> User | None:
        stmt = (
            select(User)
            .join(TgVerified, TgVerified.user_id == User.id)
            .where(TgVerified.tg_id == tg_id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def search(
            self, field: str,
            value: Any,
            strict: bool = False,
            offset: int | None = None,
            limit: int | None = None
    ) -> list[User]:

        stmt = (
            select(User)
            .join(Settings, Settings.user_id == User.id)
            .where(Settings.is_profile_public == False)
        )

        stmt = self.process_search_stmt(stmt, strict, field, value)
        stmt = self.process_paginate_stmt(stmt, limit, offset)

        result = await self.session.execute(stmt)

        return [user for user in result.scalars()]






