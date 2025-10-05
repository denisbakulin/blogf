from fastapi import APIRouter, Depends
from user.deps import userDep
from chat.schemas import  MessageCreate, DirectMessageShow, DirectChatShow
from auth.deps import verifiedUserDep
from auth.deps import currentUserDep

from chat.deps import directChatServiceDep
from helpers.search import Pagination


direct_router = APIRouter(prefix="/direct", tags=["💭 Личные сообщения"])

@direct_router.get(
    "",
    summary="Получить чаты с пользователями",
    response_model=list[DirectChatShow]
)
async def get_user_chats(
        user: currentUserDep,
        direct_service: directChatServiceDep,
        pagination: Pagination = Depends()
):
    return await direct_service.get_user_chats(user, pagination)


@direct_router.post(
    "/{username}",
    summary="Отправить сообщение пользователю",
    response_model=DirectMessageShow
)
async def create_message(
        sender: verifiedUserDep,
        recipient: userDep,
        chat_service: directChatServiceDep,
        message_info: MessageCreate

):

    return await chat_service.create_message(sender, recipient, message_info)


@direct_router.get(
    "/{username}",
    summary="Получить сообщения чата с пользователем",
    response_model=list[DirectMessageShow]
)
async def get_messages(
        user: verifiedUserDep,
        interlocutor: userDep,
        chat_service: directChatServiceDep,
        pagination: Pagination = Depends()
):

    return await chat_service.get_messages(user, interlocutor, pagination)


