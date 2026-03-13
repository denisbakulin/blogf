from deps.auth import currentUserDep
from deps.channel import *
from deps.reaction import reactionServiceDep
from entities.reaction import ReactionType
from fastapi import APIRouter, Depends
from helpers.search import Pagination
from schemas.channel import ChannelCreate
from schemas.container import ContainerShow

router = APIRouter(prefix="/channels", tags=["📚 Каналы"])


@router.post(
    "",
    summary="Создать канал",
    response_model=ContainerShow
)
async def create_channel(
        channel: ChannelCreate,
        user: currentUserDep,
        service: channelServiceDep
):
    return await service.create_channel(user_id=user.id, channel=channel)




@router.get(
    "/{slug}",
    summary="Посмотреть канал",
)
async def get_channel(
        channel: channelDep
):
    return channel


@router.post(
    "/{slug}/join",
    summary="Отправить заявку в приватный канал"
)
async def send_join_request(
        container: privateChannelDep,
        service: privateChannelServiceDep,
        user: currentUserDep,
):
    return await service.send_jr(
        channel_id=container.id, user_id=user.id
    )


@router.get(
    "/{slug}/join",
    summary="Получить заявки в канал",
)
async def get_jrs(
        service: privateChannelServiceDep,
        user: currentUserDep,
        channel: privateChannelDep,
        pagination: Pagination = Depends()
):
    return await service.get_jrs(user_id=user.id, container=channel, pagination=pagination)

@router.post(
    "/join-process/{jr_id}",
    summary="Обработать заявку"
)
async def process_jr(
        service: privateChannelServiceDep,
        user: currentUserDep,
        jr_id: int,
        approve: bool
):
    await service.process_jr(user_id=user.id, jr_id=jr_id, approve=approve)


@router.get(
    "/{slug}/subscribe",
    summary="Получить подписчиков канала",
)
async def process_subscribe(
        service: channelServiceDep,
        user: currentUserDep,
        channel: channelDep,
        pagination: Pagination = Depends()
):
    return await service.get_subscribers(container=channel, pagination=pagination)


@router.post(
    "/{slug}/subscribe",
    summary="Подписаться на публичный канал",
)
async def create_subscribe(
        service: publicChannelServiceDep,
        user: currentUserDep,
        channel: publicChannelDep,
):
    return await service.subscribe(user_id=user.id, channel_id=channel.id)





@router.post(
    "/{slug}/reactions",
    summary="Оставить реакцию под каналом",
)
async def set_channel_reactions(
        channel: channelDep,
        user: currentUserDep,
        reaction: ReactionType,
        service: reactionServiceDep
):
    return await service.process_container_reaction(user_id=user.id, container_id=channel.id, reaction=reaction)
