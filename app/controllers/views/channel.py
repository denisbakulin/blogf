from deps.auth import currentUserDep
from deps.channel import *
from fastapi import APIRouter, Depends
from helpers.search import Pagination
from schemas.channel import ChannelCreate
from schemas.container import ContainerShow, ContainerUpdate
from base.db import getSessionDep
from usecases.post import GetPostsUseCase, CreatePostUseCase
from usecases.container import UpdateContainerUseCase
from schemas.post import PostCreate

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

@router.patch(
    "/{slug}",
    summary="Изменить канал",
)
async def update_channel(
        channel: channelDep,
        update: ContainerUpdate,
        session: getSessionDep,
        user: currentUserDep
):
    logic = UpdateContainerUseCase(session)

    return await logic.execute(
        user=user, container_id=channel.id, update=update
    )


@router.get(
    "/{slug}/posts",
    summary="Получить посты канала",
)
async def get_channel_posts(
        channel: channelDep,
        session: getSessionDep,
        user: currentUserDep,
        pagination: Pagination = Depends()

):
    logic = GetPostsUseCase(session)

    return await logic.execute(
        container_id=channel.id, user=user, pagination=pagination
    )

@router.post(
    "/{slug}/posts",
    summary="Создать пост в канале",
)
async def create_channel_post(
        channel: channelDep,
        session: getSessionDep,
        user: currentUserDep,
        create: PostCreate
):
    logic = CreatePostUseCase(session)

    return await logic.execute(
        container_id=channel.id, user=user, post=create
    )






@router.post(
    "/{slug}/join",
    summary="Отправить заявку в приватный канал"
)
async def send_join_request(
        channel: privateChannelDep,
        service: privateChannelServiceDep,
        user: currentUserDep,
):
    return await service.send_jr(
        channel_id=channel.id, user_id=user.id
    )


@router.get(
    "/{slug}/join",
    summary="Получить заявки в канал",
)
async def get_jrs(
        channel: privateChannelDep,
        service: privateChannelServiceDep,
        user: currentUserDep,
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
    "/{slug}/subscribers",
    summary="Получить подписчиков канала",
)
async def process_subscribe(
        service: channelServiceDep,
        user: currentUserDep,
        channel: channelDep,
        pagination: Pagination = Depends()
):
    return await service.get_subscribers(
        user_id=user.id,container=channel, pagination=pagination
    )


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

