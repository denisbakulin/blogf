from base.db import getSessionDep
from deps.auth import currentUserDep
from fastapi import APIRouter, Depends
from helpers.search import Pagination
from schemas.container import ContainerShow, ContainerUpdate
from schemas.post import PostCreate, PostAuthorShow, UserUsername, PostShow
from logic import UpdateContainerUseCase, CreatePostUseCase, GetPostsUseCase, GetChannelUseCase
from schemas.user import UserShow

from logic.channel import  GetChannelSubscribersUseCase

router = APIRouter(prefix="/{channel_id}")


@router.get(
    "",
    summary="Посмотреть канал",
    response_model=ContainerShow
)
async def get_channel(
    channel_id: int,
    session: getSessionDep,
    user: currentUserDep
):
    logic = GetChannelUseCase(session)

    channel = await logic.execute(channel_id=channel_id, user=user)

    return ContainerShow.from_orm(channel)




@router.patch(
    "",
    summary="Изменить канал",
)
async def update_channel(
    channel_id: int,
    update: ContainerUpdate,
    session: getSessionDep,
    user: currentUserDep
):
    logic = UpdateContainerUseCase(session)

    return await logic.execute(
        user=user, container_id=channel_id, update=update
    )


@router.get(
    "/posts",
    tags=["Posts"],
    summary="Получить посты канала",
    response_model=list[PostAuthorShow]
)
async def get_channel_posts(
    channel_id: int,
    session: getSessionDep,
    user: currentUserDep,
    pagination: Pagination = Depends()
):
    logic = GetPostsUseCase(session)

    posts = await logic.execute(
        container_id=channel_id, user=user, pagination=pagination
    )

    return [
        PostAuthorShow(
            **PostShow.from_orm(post).model_dump(),
            author=UserUsername.from_orm(author)
        ) for post, author in posts
    ]

@router.post(
    "/posts",
    tags=["Posts"],
    summary="Создать пост в канале",
    response_model=PostShow
)
async def create_channel_post(
    channel_id: int,
    session: getSessionDep,
    user: currentUserDep,
    create: PostCreate
):
    logic = CreatePostUseCase(session)

    post = await logic.execute(
        container_id=channel_id, user=user, post=create
    )

    return PostShow.from_orm(post)



@router.get(
    "/subscribers",
    tags=["Subscribe"],
    summary="Получить подписчиков канала",
    response_model=list[UserShow]
)
async def process_subscribe(
    channel_id: int,
    session: getSessionDep,
    user: currentUserDep,
    pagination: Pagination = Depends()
):
    logic = GetChannelSubscribersUseCase(session)

    users = await logic.execute(
        user=user, channel_id=channel_id, pagination=pagination
    )

    return [
        UserShow.from_orm(user) for user in users
    ]








