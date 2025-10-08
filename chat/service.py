from sqlalchemy.ext.asyncio import AsyncSession

from core.service import BaseService
from user.model import User
from chat.model import DirectMessage, DirectChat

from chat.repository import DirectChatRepository
from chat.schemas import MessageCreate
from helpers.search import Pagination
from core.repository import BaseRepository
from chat.manager import WebSocketManager
from core.exceptions import EntityNotFoundError, EntityLockedError, EntityBadRequestError

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
            chat = await self.create_item(
                first_user_id=sender.id, second_user_id=recipient.id
            )

        if chat.banned_user_id is not None:
            raise EntityLockedError(f"Чат [{sender.username} - {recipient.username}]")

        message = await self.message_service.create_item(
            sender_id=sender.id,
            recipient_id=recipient.id,
            content=message_info.content
        )

        await self.ws_manager.message_notify(
            recipient_id=recipient.id,
            message_id=message.id,
            message=message.content[:50],
            username=sender.username
        )

        return message

    async def ban_direct(
            self,
            current_user: User,
            to_ban_user: User
    ):
        chat = await self.get_direct(current_user, to_ban_user)

        if chat.banned_user_id:
            raise EntityBadRequestError(str(chat), "Чат уже заблокирован")

        await self.update_item(chat, banned_user_id=current_user.id)

    async def unban_direct(
            self,
            current_user: User,
            to_unban_user: User
    ):
        chat = await self.get_direct(current_user, to_unban_user)

        if chat.banned_user_id != current_user.id:
            raise EntityBadRequestError(str(chat), "Невозможно разблокировать чат")

        await self.update_item(chat, banned_user_id=None)




    async def get_user_chats(self, user: User, pagination: Pagination) -> list[DirectChat]:
        return await self.repository.get_user_chats(user_id=user.id, **pagination.get())

    async def get_message_by_id(self, user: User, message_id: int) -> DirectMessage:
        message = await self.message_service.get_item_by_id(message_id)

        if user.id not in (message.recipient_id, message.sender_id):
            raise EntityNotFoundError("Сообщение", id=message_id)

        return message





    async def get_direct(self, user1: User, user2: User) -> DirectChat:
        direct = await self.repository.chat_exists(user1.id, user2.id)

        if direct:
            return direct

        raise EntityNotFoundError(
            "direct",
            username1=user1.username,
            username2=user2.username
        )

    async def get_banned_chats(
            self,
            user: User,
            pagination: Pagination
    ):
        return await self.repository.get_any_by(
            banned_user_id=user.id, **pagination.get()
        )
