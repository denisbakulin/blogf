from typing import Annotated

# from deps.post import postServiceDep
from fastapi import APIRouter, Depends

from deps.auth import currentUserDep
from deps.comment import commentServiceDep
from deps.container import containerServiceDep
from deps.subscribe import subscribeServiceDep
from deps.user import userDep, userLogicDep, userServiceDep
from entities.container import Container, ContainerType
from helpers.search import Pagination
from schemas.container import ContainerShow
# from schemas.post import PostShow
# from schemas.topic import UserCommentsCountOfTopicShow
from schemas.user import UserProfileShow, UserShow
from usecases.post import GetWallPostsUseCase
from utils.user import UserSearchParams

user_router = APIRouter(prefix="/users", tags=["👨 Пользователи"])

@user_router.get(
    "/search",
    summary="Поиск пользователя по ключевым параметрам",
    response_model=list[UserShow],
)
async def search_users(
        service: userServiceDep,
        search: UserSearchParams = Depends(),
        pagination: Pagination = Depends(),
):
    return await service.search_users(search=search, pagination=pagination)



@user_router.get(
    "/@{username}",
    summary="Получить пользователя по username",
    response_model=UserProfileShow,
)
async def get_user(
        user: userDep,
        logic: userLogicDep
):
    return await logic.get_profile(user)


@user_router.get(
    "/@{username}/top-topics",
    summary="Получить топ обсуждений пользователя",
)
async def get_top_topics(
        user: userDep,
        service: commentServiceDep,
):
    return await service.get_top_themes_of_user(user.id)


@user_router.get(
    "/@{username}/wall",
    summary="Получить стену пользователя",
)
async def get_user_wall(
        user: userDep,
        service: containerServiceDep,
):
    return await service.get_by_or_raise(author_id=user.id, type=ContainerType.wall)

from base.db import getSessionDep


@user_router.get(
    "/@{username}/wall/posts",
    summary="Получить посты пользователя",
)#todo
async def get_user_wall_posts(
        wall_owner: userDep,
        session: getSessionDep,
        pagination: Pagination = Depends(),
):
    uc = GetWallPostsUseCase(session)
    return await uc.execute(wall_owner_id=wall_owner.id, pagination=pagination)


@user_router.get(
    "/@{username}/wall/subscribe",
    summary="Подписаться на пользователя",
)
async def subscribe_to_user_wall(
        user: userDep,
        service: subscribeServiceDep,
        c: containerServiceDep
):
    container = await c.get_by_or_raise(author_id=user.id, type=ContainerType.wall)
    return await service.create_subscribe(user_id=user.id, container_id=container.id)








