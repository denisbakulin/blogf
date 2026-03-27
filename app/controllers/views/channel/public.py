from base.db import getSessionDep
from deps.auth import currentUserDep
from deps.channel import *
from fastapi import APIRouter, Depends, status
from helpers.search import Pagination
from schemas.admin import AdminCreate
from schemas.container import ContainerShow, ContainerUpdate
from schemas.post import PostCreate, PostAuthorShow, UserUsername, PostShow
from logic import UpdateContainerUseCase, CreatePostUseCase, GetPostsUseCase
from schemas.user import UserShow

from logic.channel import  GetChannelSubscribersUseCase

router = APIRouter(prefix="/{slug}", tags=["Public"])


@router.get(
    "",
    summary="Посмотреть канал",
    response_model=ContainerShow
)
async def get_channel(
    channel: publicChannelDep
):
    return ContainerShow.from_orm(channel)


@router.patch(
    "",
    summary="Изменить канал",
)
async def update_channel(
    channel: publicChannelDep,
    update: ContainerUpdate,
    session: getSessionDep,
    user: currentUserDep
):
    logic = UpdateContainerUseCase(session)

    return await logic.execute(
        user=user, container_id=channel.id, update=update
    )


@router.get(
    "/posts",
    summary="Получить посты канала",
    response_model=list[PostAuthorShow]
)
async def get_channel_posts(
    channel: publicChannelDep,
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
    "/posts",
    summary="Создать пост в канале",
    response_model=PostShow
)
async def create_channel_post(
    channel: publicChannelDep,
    session: getSessionDep,
    user: currentUserDep,
    create: PostCreate
):
    logic = CreatePostUseCase(session)

    post = await logic.execute(
        container_id=channel.id, user=user, post=create
    )
    return PostShow.from_orm(post)



@router.get(
    "/subscribers",
    summary="Получить подписчиков канала",
    response_model=list[UserShow]
)
async def process_subscribe(
    session: getSessionDep,
    user: currentUserDep,
    channel: publicChannelDep,
    pagination: Pagination = Depends()
):
    logic = GetChannelSubscribersUseCase(session)

    users = await logic.execute(user_id=user.id, channel=channel, pagination=pagination)

    return [
        UserShow.from_orm(user) for user in users
    ]




@router.post(
    "/subscribe",
    summary="Подписаться на публичный канал",
    status_code=status.HTTP_201_CREATED
)
async def create_subscribe(
    service: publicChannelServiceDep,
    user: currentUserDep,
    channel: publicChannelDep,
):
    return await service.subscribe(user_id=user.id, channel_id=channel.id)





