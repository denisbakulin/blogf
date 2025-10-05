from sqlalchemy.ext.asyncio import AsyncSession

from core.service import BaseService
from user.model import User
from chat.model import DirectMessage, DirectChat

from chat.repository import DirectChatRepository
from chat.schemas import MessageCreate, DirectChatShow
from helpers.search import Pagination


class DirectChatService(BaseService[DirectChat, DirectChatRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(DirectChat, session, DirectChatRepository)


    async def create_message(
            self,
            sender: User,
            recipient: User,
            message_info: MessageCreate
    ) -> DirectMessage:
        chat = await self.repository.chat_exists(sender.id, recipient.id)

        if chat is None:
            await self.create_item(
                first_user_id=sender.id, second_user_id=recipient.id
            )

        message = self.repository.message.create(
            sender_id=sender.id,
            recipient_id=recipient.id,
            content=message_info.content
        )

        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def get_messages(
            self,
            user: User,
            interlocutor: User,
            pagination: Pagination
    ) -> list[DirectMessage]:

        return await self.repository.message.get_any_by(
            sender_id=user.id, recipient_id=interlocutor.id, **pagination.get()
        )

    async def get_user_chats(self, user: User, pagination: Pagination) -> list[DirectChat]:
        return await self.repository.get_user_chats(user_id=user.id, **pagination.get())




