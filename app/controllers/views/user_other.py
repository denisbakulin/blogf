from base.db import getSessionDep
from deps.auth import currentUserDep
from services.comment import CommentService
from deps.container import containerServiceDep
from services.subscribe import SubscribeService
from deps.user import userServiceDep
from entities import ContainerType
from fastapi import APIRouter, Depends, status
from helpers.search import Pagination
from schemas.container import ContainerMetricsShow
from schemas.post import PostShow
from schemas.user import UserProfile, UserProfileShow, UserShow
from logic import GetWallPostsUseCase
from utils.user import UserSearchParams


router = APIRouter(prefix="/users", tags=["👨 Пользователи"])

@router.get(
    "/search",
    summary="Поиск пользователя по ключевым параметрам",
    response_model=list[UserShow],
)
async def search_users(
    service: userServiceDep,
    search: UserSearchParams = Depends(),
    pagination: Pagination = Depends(),
):
    users = await service.search_users(search=search, pagination=pagination)

    return [
        UserShow.from_orm(user)
        for user in users
    ]


@router.get(
    "/{user_id}",
    summary="Получить пользователя по username",
    response_model=UserProfileShow,
)
async def get_user(
    user_id: int,
    service: userServiceDep
):
    user = await service.get_user_by_id(user_id)
    profile = await service.get_user_profile(user_id)

    return UserProfileShow(
        **UserShow.from_orm(user).model_dump(),
        profile=UserProfile.from_orm(profile)
    )


from schemas.topic import UserCommentsCountOfTopicShow


@router.get(
    "/{user_id}/top-topics",
    summary="Получить топ обсуждений пользователя по кол-ву комментариев",
    response_model=list[UserCommentsCountOfTopicShow]
)
async def get_top_topics(
    user_id: int,
    session: getSessionDep,
):
    service = CommentService(session)

    top = await service.get_top_themes_of_user(user_id)

    return [
        UserCommentsCountOfTopicShow(topic_slug=topic.slug, count=count)
        for topic, count in top
    ]



@router.get(
    "/{user_id}/wall",
    summary="Получить стену пользователя",
    response_model=ContainerMetricsShow
)
async def get_user_wall(
    user_id: int,
    service: containerServiceDep,
):
    wall = await service.get_by_or_raise(
        author_id=user_id, type=ContainerType.WALL
    )

    return ContainerMetricsShow.from_orm(wall)


@router.get(
    "/{user_id}/wall/posts",
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


@router.post(
    "/{user_id}/wall/subscribe",
    summary="Подписаться на пользователя",
    status_code=status.HTTP_201_CREATED,
    response_model=None
)
async def subscribe_to_user_wall(
    user_id: int,
    cuser: currentUserDep,
    session: getSessionDep,
    c: containerServiceDep
):
    service = SubscribeService(session)
    container = await c.get_by_or_raise(author_id=user_id, type=ContainerType.WALL)
    return await service.create_subscribe(user_id=cuser.id, container_id=container.id)








