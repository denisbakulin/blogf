from sqlalchemy.ext.asyncio import AsyncSession

from core.service import BaseService
from user.model import User
from chat.model import DirectMessage, DirectChat

from chat.repository import DirectChatRepository
from chat.schemas import MessageCreate
from helpers.search import Pagination
from core.repository import BaseRepository
from chat.manager import WebSocketManager
from core.exceptions import EntityNotFoundError


class DirectMessageService(BaseService[DirectMessage, BaseRepository]):
    def __init__(self, session: AsyncSession):
        super().__init__(DirectMessage, session)

    async def get_messages(
            self,
            user: User,
            interlocutor: User,
            pagination: Pagination
    ) -> list[DirectMessage]:

        return await self.repository.get_any_by(
            sender_id=user.id, recipient_id=interlocutor.id, **pagination.get()
        )



class DirectChatService(BaseService[DirectChat, DirectChatRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(DirectChat, session, DirectChatRepository)
        self.message_service = DirectMessageService(session)
        self.ws_manager = WebSocketManager()




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

        message = await self.message_service.create_item(
            sender_id=sender.id,
            recipient_id=recipient.id,
            content=message_info.content
        )

        await self.ws_manager.message_notify(
            recipient_id=recipient.id,
            message_id=message.id,
            message=message.content[:100],
            username=sender.username
        )

        return message


    async def get_user_chats(self, user: User, pagination: Pagination) -> list[DirectChat]:
        return await self.repository.get_user_chats(user_id=user.id, **pagination.get())

    async def get_message_by_id(self, user: User, message_id: int) -> DirectMessage:
        message = await self.message_service.get_item_by_id(message_id)

        if user.id not in (message.recipient_id, message.sender_id):
            raise EntityNotFoundError("Сообщение", id=message_id)

        return message

