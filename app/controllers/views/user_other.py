from deps.comment import commentServiceDep
from deps.container import containerServiceDep
from deps.subscribe import subscribeServiceDep
from deps.user import userDep, userLogicDep, userServiceDep
from deps.auth import currentUserDep
from entities.container import ContainerType
from fastapi import APIRouter, Depends, status
from helpers.search import Pagination


from schemas.user import UserProfileShow, UserShow
from usecases.post import GetWallPostsUseCase
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
    return await service.search_users(search=search, pagination=pagination)



@router.get(
    "/@{username}",
    summary="Получить пользователя по username",
    response_model=UserProfileShow,
)
async def get_user(
        user: userDep,
        logic: userLogicDep
):
    return await logic.get_profile(user)


@router.get(
    "/@{username}/top-topics",
    summary="Получить топ обсуждений пользователя",
)
async def get_top_topics(
        user: userDep,
        service: commentServiceDep,
):
    return await service.get_top_themes_of_user(user.id)


@router.get(
    "/@{username}/wall",
    summary="Получить стену пользователя",
)
async def get_user_wall(
        user: userDep,
        service: containerServiceDep,
):
    return await service.get_by_or_raise(author_id=user.id, type=ContainerType.WALL)

from base.db import getSessionDep


@router.get(
    "/@{username}/wall/posts",
    summary="Получить посты пользователя",
)
async def get_user_wall_posts(
        wall_owner: userDep,
        session: getSessionDep,
        pagination: Pagination = Depends(),
):
    logic = GetWallPostsUseCase(session)
    return await logic.execute(wall_owner_id=wall_owner.id, pagination=pagination)


@router.post(
    "/@{username}/wall/subscribe",
    summary="Подписаться на пользователя",
    status_code=status.HTTP_201_CREATED
)
async def subscribe_to_user_wall(
        user: userDep,
        cuser: currentUserDep,
        service: subscribeServiceDep,
        c: containerServiceDep
):
    container = await c.get_by_or_raise(author_id=user.id, type=ContainerType.WALL)
    return await service.create_subscribe(user_id=cuser.id, container_id=container.id)








