from base.db import getSessionDep
from deps.auth import currentUserDep
from deps.comment import commentServiceDep
from deps.container import containerServiceDep
from deps.subscribe import subscribeServiceDep
from deps.user import userDep, userServiceDep
from entities import ContainerType
from fastapi import APIRouter, Depends, status
from helpers.search import Pagination
from schemas.container import WallShow
from schemas.post import PostShow
from schemas.user import UserProfile, UserProfileShow, UserShow
from logic import GetWallPostsUseCase
from utils.user import UserSearchParams


router = APIRouter(prefix="/users/{username}", tags=["👨 Пользователи"])

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
    "",
    summary="Получить пользователя по username",
    response_model=UserProfileShow,
)
async def get_user(
        user: userDep,
        service: userServiceDep
):
    profile = await service.get_user_profile(user.id)

    return UserProfileShow(
        **UserShow.from_orm(user).model_dump(),
        profile=UserProfile.from_orm(profile)
    )


from schemas.topic import UserCommentsCountOfTopicShow


@router.get(
    "/top-topics",
    summary="Получить топ обсуждений пользователя по кол-ву комментариев",
    response_model=list[UserCommentsCountOfTopicShow]
)
async def get_top_topics(
        user: userDep,
        service: commentServiceDep,
):
    top = await service.get_top_themes_of_user(user.id)

    return [
        UserCommentsCountOfTopicShow(topic_slug=topic.slug, count=count)
        for topic, count in top
    ]



@router.get(
    "/wall",
    summary="Получить стену пользователя",
    response_model=WallShow
)
async def get_user_wall(
        user: userDep,
        service: containerServiceDep,
):
    wall = await service.get_by_or_raise(
        author_id=user.id, type=ContainerType.WALL
    )

    return WallShow.from_orm(wall)




@router.get(
    "/wall/posts",
    summary="Получить посты пользователя",
    response_model=list[PostShow]
)
async def get_user_wall_posts(
        wall_owner: userDep,
        session: getSessionDep,
        pagination: Pagination = Depends(),
):
    logic = GetWallPostsUseCase(session)

    posts = await logic.execute(wall_owner_id=wall_owner.id, pagination=pagination)

    return [
        PostShow.from_orm(post)
        for post in posts
    ]


@router.post(
    "/wall/subscribe",
    summary="Подписаться на пользователя",
    status_code=status.HTTP_201_CREATED,
    response_model=None
)
async def subscribe_to_user_wall(
        user: userDep,
        cuser: currentUserDep,
        service: subscribeServiceDep,
        c: containerServiceDep
):
    container = await c.get_by_or_raise(author_id=user.id, type=ContainerType.WALL)
    return await service.create_subscribe(user_id=cuser.id, container_id=container.id)








