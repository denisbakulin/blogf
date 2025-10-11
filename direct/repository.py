from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_, case
from sqlalchemy.orm import aliased

from core.repository import BaseRepository
from direct.model import DirectChat

from typing import Optional

from user.model import User
from direct.model import DirectUserSettings


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

    async def get_user_chats(self, user_id: int, offset: int, limit: int) -> list[tuple[DirectUserSettings, User]]:
        """Возвращает чаты пользователя в виде
        [("название чата", User - собеседник)]"""

        companion_id_case = case(
            (DirectChat.first_user_id == user_id, DirectChat.second_user_id),
            else_=DirectChat.first_user_id
        )

        stmt = (
            select(
                DirectUserSettings,
                User
            )
            .select_from(DirectChat)
            .where(
                or_(
                    DirectChat.first_user_id == user_id,
                    DirectChat.second_user_id == user_id,
                )
            )
            .join(
                DirectUserSettings,
                DirectUserSettings.chat_id == DirectChat.id
            )
            .join(
                User,
                User.id == companion_id_case,
            )

            .offset(offset)
            .limit(limit)
        )

        result = await self.session.execute(stmt)

        return list(result.tuples().all())




