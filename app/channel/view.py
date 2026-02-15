from fastapi import APIRouter, Depends

from channel.deps import channelServiceDep, channelDep

from container.schemas import ContainerShow
from channel.schemas import ChannelCreate
from auth.deps import currentUserDep
from helpers.search import Pagination

from join_request.schemas import JRShow
from sub.schemas import SubscriberOfContainerShow

channel_router = APIRouter(prefix="/channels", tags=["📚 Каналы"])



@channel_router.post(
    "",
    summary="Создать канал",
    response_model=ContainerShow
)
async def create_channel(
        container: ChannelCreate,
        user: currentUserDep,
        service: channelServiceDep
):
    return await service.create_channel(user=user, channel=container)


@channel_router.get(
    "/{slug}",
    summary="Посмотреть канал",
    response_model=ContainerShow
)
async def get_channel(
        channel: channelDep
):
    return channel


@channel_router.post(
    "/{slug}/join",
    summary="Отправить заявку в приватный канал"
)
async def send_join_request(
        container: channelDep,
        service: channelServiceDep,
        user: currentUserDep,
):
    return await service.private.send_jr(
        container=container, user=user
    )


@channel_router.get(
    "/{slug}/join",
    summary="Получить заявки в канал",
    response_model=list[JRShow]
)
async def get_jrs(
        service: channelServiceDep,
        user: currentUserDep,
        container: channelDep,
        pagination: Pagination = Depends()
):
    return await service.private.get_jrs(user=user, container=container, pagination=pagination)

@channel_router.post(
    "/join-process/{jr_id}",
    summary="Обработать заявку"
)
async def process_jr(
        service: channelServiceDep,
        user: currentUserDep,
        jr_id: int,
        approve: bool
):
    await service.private.process_jr(user=user, jr_id=jr_id, approve=approve)

@channel_router.get(
    "/{slug}/sub",
    summary="Получить подписчиков канала",
    response_model=list[SubscriberOfContainerShow]
)
async def process_subscribe(
        service: channelServiceDep,
        user: currentUserDep,
        channel: channelDep,
        pagination: Pagination = Depends()
):
    return await service.get_subscribers(user=user, container=channel, pagination=pagination)


@channel_router.post(
    "/{slug}/sub",
    summary="Подписаться на публичный канал",
)
async def create_subscribe(
        service: channelServiceDep,
        user: currentUserDep,
        channel: channelDep,
):
    return await service.public.subscribe(user=user, container=channel)