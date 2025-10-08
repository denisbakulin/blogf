from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, all_, or_, and_

from core.repository import BaseRepository
from direct.model import DirectMessage, DirectChat

from typing import Optional


class DirectChatRepository(BaseRepository):

    def __init__(self, session: AsyncSession):
        super().__init__(DirectChat, session)



    async def chat_exists(self, id1: int, id2: int) -> Optional[DirectChat]:
        stmt = (
            select(DirectChat)
            .where(
                or_(
                    and_(DirectChat.first_user_id == id1, DirectChat.second_user_id == id2),
                    and_(DirectChat.first_user_id == id2, DirectChat.second_user_id == id1)
                )
            )
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_user_chats(self, user_id: int, offset: int, limit: int) -> list[DirectChat]:
        stmt = (
            select(DirectChat)
            .where(
                or_(
                    and_(DirectChat.first_user_id == user_id),
                    and_(DirectChat.second_user_id == user_id)
                )
            )
            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(stmt)

        return list(result.scalars().all())




