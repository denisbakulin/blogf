from base.db import getSessionDep
from deps.auth import currentUserDep
from deps.channel import *
from fastapi import APIRouter, Depends, status
from helpers.search import Pagination
from schemas.admin import AdminCreate
from schemas.channel import ChannelCreate
from schemas.container import ContainerShow, ContainerUpdate
from schemas.post import PostCreate, PostAuthorShow, UserUsername, PostShow
from usecases.container import UpdateContainerUseCase
from usecases.post import CreatePostUseCase, GetPostsUseCase
from schemas.join_request import JRShow, JRSUserShow
from schemas.user import UserShow

from usecases.channel import CreateChannelUseCase, GetChannelSubscribersUseCase, SetChannelAdminUseCase

router = APIRouter(prefix="/channels", tags=["📚 Каналы"])


@router.post(
    "",
    summary="Создать канал",
    status_code=status.HTTP_201_CREATED,
    response_model=ContainerShow
)
async def create_channel(
    create: ChannelCreate,
    user: currentUserDep,
    session: getSessionDep
):
    logic = CreateChannelUseCase(session)

    channel = await logic.execute(user_id=user.id, create=create)

    return ContainerShow.from_orm(channel)


@router.get(
    "/{slug}",
    summary="Посмотреть канал",
    response_model=ContainerShow
)
async def get_channel(
        channel: channelDep
):
    return ContainerShow.from_orm(channel)

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
    response_model=list[PostAuthorShow]
)
async def get_channel_posts(
    channel: channelDep,
    session: getSessionDep,
    user: currentUserDep,
    pagination: Pagination = Depends()

):
    logic = GetPostsUseCase(session)

    posts = await logic.execute(
        container_id=channel.id, user=user, pagination=pagination
    )

    return [
        PostAuthorShow(
            **PostShow.from_orm(post).model_dump(),
            author=UserUsername.from_orm(author)
        ) for post, author in posts
    ]

@router.post(
    "/{slug}/posts",
    summary="Создать пост в канале",
    response_model=PostShow
)
async def create_channel_post(
    channel: channelDep,
    session: getSessionDep,
    user: currentUserDep,
    create: PostCreate
):
    logic = CreatePostUseCase(session)

    post = await logic.execute(
        container_id=channel.id, user=user, post=create
    )
    return PostShow.from_orm(post)





@router.post(
    "/{slug}/join",
    summary="Отправить заявку в приватный канал",
    status_code=status.HTTP_201_CREATED
)
async def send_join_request(
    channel: privateChannelDep,
    service: privateChannelServiceDep,
    user: currentUserDep,
):
    await service.send_jr(
        channel_id=channel.id, user_id=user.id
    )


@router.get(
    "/{slug}/join",
    summary="Получить заявки в канал",
    response_model=list[JRSUserShow]
)
async def get_jrs(
    channel: privateChannelDep,
    service: privateChannelServiceDep,
    user: currentUserDep,
):
    jrs = await service.get_jrs(user_id=user.id, channel=channel)

    return [
        JRSUserShow(
            **JRShow.from_orm(jr).model_dump(),
            user=UserUsername.from_orm(user)
        ) for jr, user in jrs
    ]


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
    response_model=list[UserShow]
)
async def process_subscribe(
    session: getSessionDep,
    user: currentUserDep,
    channel: channelDep,
    pagination: Pagination = Depends()
):
    logic = GetChannelSubscribersUseCase(session)

    users = await logic.execute(user_id=user.id, channel=channel, pagination=pagination)

    return [
        UserShow.from_orm(user) for user in users
    ]




@router.post(
    "/{slug}/subscribe",
    summary="Подписаться на публичный канал",
    status_code=status.HTTP_201_CREATED
)
async def create_subscribe(
    service: publicChannelServiceDep,
    user: currentUserDep,
    channel: publicChannelDep,
):
    return await service.subscribe(user_id=user.id, channel_id=channel.id)



@router.post(
    "/{slug}/admin",
    summary="set admin",
    status_code=status.HTTP_201_CREATED
)
async def set_channel_admin(
    session: getSessionDep,
    user: currentUserDep,
    channel: channelDep,
    admin: AdminCreate
):
    logic = SetChannelAdminUseCase(session)

    await logic.execute(user_id=user.id, channel=channel, admin=admin)
