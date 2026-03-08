from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from base.repository import BaseRepository
from entities.container import Container
from entities.join_request import JoinRequest
from entities.user import User


class JoinRequestRepository(BaseRepository[JoinRequest]):

    def __init__(self, session: AsyncSession):
        super().__init__(JoinRequest, session)


    #todo получение запросов по группе

    async def get_jr_by_channel_id(self, channel_id: int) -> list[tuple[JoinRequest, User]]:
        stmt = (
            select(JoinRequest, User)
            .join(User, User.id == JoinRequest.user_id)
            .where(JoinRequest.container_id == channel_id)
        )

        result = await self.session.execute(stmt)

        return [
            (jr, user)
            for jr, user in result.all()
        ]







