from base.repository import BaseRepository
from entities.user import User, Profile, Settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from typing import Any

class ProfileRepository(BaseRepository[Profile]):
    def __init__(self, session: AsyncSession):
        super().__init__(Profile, session)


class SettingsRepository(BaseRepository[Settings]):
    def __init__(self, session: AsyncSession):
        super().__init__(Settings, session)



class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)


    async def search(
            self, field: str,
            value: Any,
            strict: bool = False,
            offset: int | None = None,
            limit: int | None = None
    ) -> list[User]:

        stmt = (
            select(
                User
            )
            .join(Settings, Settings.user_id == User.id)
            .where(Settings.is_profile_public == False)
        )

        stmt = self.process_search_stmt(stmt, strict, field, value)
        stmt = self.process_paginate_stmt(stmt, limit, offset)

        result = await self.session.execute(stmt)

        return list(user for user in result.scalars())






