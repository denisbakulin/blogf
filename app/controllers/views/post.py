from base.db import getSessionDep
from deps.auth import currentUserDep
from deps.post import postServiceDep

from entities import ContainerType, ReactionType
from fastapi import APIRouter, Depends, status
from helpers.search import Pagination

from schemas.post import PostShow, PostUpdate, PostContainerShow, ContainerShow, PostCreate, PostAuthorShow

from logic import (
    GetPostUseCase,
    UpdatePostUseCase,
    DeletePostUseCase,
    CreatePostUseCase,
    GetPostsUseCase, CreateWallPostUseCase, GetWallPostsUseCase

)
from utils.post import PostSearchParams
from schemas.reaction import UserUsername


router = APIRouter(prefix="/posts", tags=["📝 Посты"])


@router.get(
    "/top",
    summary="Получить топ постов",
)
async def get_top_of_posts(
        service: postServiceDep,
):
    return await service.repository.get_top_of_container_posts(
        container_type=ContainerType.TOPIC, reaction_type=ReactionType.LIKE
    )



@router.get(
    "/search",
    summary="Поиск поста по ключевым параметрам",
)
async def search_posts(
        post_service: postServiceDep,
        search: PostSearchParams = Depends(),
        pagination: Pagination = Depends()
):
    return await post_service.search_items(search=search, pagination=pagination)



@router.get(
    "/{post_id}",
    summary="Получить пост",
    response_model=PostContainerShow,
)
async def get_post(
        post_id: int,
        session: getSessionDep,
        user: currentUserDep,
):
    logic = GetPostUseCase(session)

    post, container = await logic.execute(user=user, post_id=post_id)

    return PostContainerShow(
        **PostShow.from_orm(post).model_dump(),
        container=ContainerShow.from_orm(container)
    )

@router.patch(
    "/{post_id}",
    summary="Изменить информацию о посте",
    response_model=PostShow
)
async def update_post(
        session: getSessionDep,
        post_id: int,
        user: currentUserDep,
        update: PostUpdate,
):
    logic = UpdatePostUseCase(session)

    return await logic.execute(
        post_id=post_id, update=update, user=user
    )


@router.delete(
    "/{post_id}",
    summary="Удалить пост",
)
async def delete_post(
        session: getSessionDep,
        post_id: int,
        user: currentUserDep,
):
    logic = DeletePostUseCase(session)

    return await logic.execute(
        post_id=post_id,  user=user
    )



@router.get(
    "/channels/{channel_id}",
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
    "/channels/{channel_id}",
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





@router.post(
    "/topics/{topic_id}",
    summary="Создать пост",
    status_code=status.HTTP_201_CREATED,
    response_model=PostShow
)
async def create_topic_post(
    topic_id: int,
    create: PostCreate,
    user: currentUserDep,
    session: getSessionDep
):
    logic = CreatePostUseCase(session)

    post = await logic.execute(
        user=user, post=create, container_id=topic_id
    )

    return PostShow.from_orm(post)


@router.get(
    "/topics/{topic_id}",
    summary="Получить посты по теме",
    response_model=list[PostAuthorShow]
)
async def get_topic_posts(
    topic_id: int,
    service: postServiceDep,
    pagination: Pagination = Depends()
):

    posts = await service.get_posts_with_authors(
        container_id=topic_id, pagination=pagination
    )

    return [
        PostAuthorShow(
            **PostShow.from_orm(post).model_dump(),
            author=UserUsername.from_orm(author)
        ) for post, author in posts
    ]



@router.post(
    "/users/{owner_id}",
    summary="Создать пост",
    status_code=status.HTTP_201_CREATED,
    response_model=PostShow
)
async def create_my_post(
    create: PostCreate,
    user: currentUserDep,
    session: getSessionDep,
    owner_id: int
):

    logic = CreateWallPostUseCase(session)
    post = await logic.execute(user=user, owner_id=owner_id, create=create)

    return PostShow.from_orm(post)




@router.get(
    "/users/{user_id}",
    summary="Получить посты пользователя",
    response_model=list[PostShow]
)
async def get_user_wall_posts(
    user_id: int,
    session: getSessionDep,
    pagination: Pagination = Depends(),
):
    logic = GetWallPostsUseCase(session)

    posts = await logic.execute(wall_owner_id=user_id, pagination=pagination)

    return [
        PostShow.from_orm(post)
        for post in posts
    ]