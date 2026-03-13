from typing import Any

from auth.oauth import OAuthUser, ProviderType
from base.repository import BaseRepository
from entities.user import Profile, Settings, User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


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
            .join(OAuthUser, OAuthUser.user_id == User.id)
            .where(OAuthUser.provider_id == tg_id)
            .where(OAuthUser.provider == ProviderType.TELEGRAM)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


    async def search(
            self,
            field: str,
            value: Any,
            strict: bool = False,
            offset: int | None = None,
            limit: int | None = None
    ) -> list[User]:

        stmt = (
            select(User)
            .join(Settings, Settings.user_id == User.id)
            .where(Settings.is_profile_public == True)
        )

        stmt = self.process_search_stmt(stmt, strict, field, value)
        stmt = self.process_paginate_stmt(stmt, offset, limit)

        result = await self.session.execute(stmt)

        return [user for user in result.scalars()]






