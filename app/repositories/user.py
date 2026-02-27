from base.repository import BaseRepository
from models.user import User, Profile, Settings
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from DTO.user import UserDTO, UserCreds, ProfileDTO, SettingsDTO

from typing import Any

class ProfileRepository(BaseRepository[Profile, ProfileDTO]):
    def __init__(self, session: AsyncSession):
        super().__init__(Profile, session, ProfileDTO)


class SettingsRepository(BaseRepository[Settings, SettingsDTO]):
    def __init__(self, session: AsyncSession):
        super().__init__(Settings, session, SettingsDTO)




class UserRepository(BaseRepository[User, UserDTO]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session, UserDTO)


    async def get_user_creds_by_username(self, username: str) -> UserCreds:
        user = await self.get_orm(username=username)

        return UserCreds(
            id=user.id,
            password=user.password
        )

    async def search(
            self, field: str,
            value: Any,
            strict: bool = False,
            offset: int | None = None,
            limit: int | None = None
    ) -> list[UserDTO]:

        stmt = (
            select(
                User
            )
            .join(Settings, Settings.user_id == User.id)
            .where(Settings.is_profile_public == False)
        )
        if strict:
            stmt = stmt.where(getattr(self.model, field) == value)
        else:
            stmt = stmt.where(getattr(self.model, field).ilike(f"%{value}%"))

        stmt = self.paginator(stmt, limit, offset)

        result = await self.session.execute(stmt)

        return list(self.to_dto(user) for user in result.scalars())






