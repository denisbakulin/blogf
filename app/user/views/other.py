from fastapi import APIRouter, Depends

from comment.deps import commentServiceDep
from helpers.search import Pagination
from post.deps import postServiceDep
from post.schemas import PostShow
from topic.release.schemas import UserCommentsCountOfTopicShow
from user.deps import userDep, userServiceDep
from user.schemas import UserShow
from user.utils import UserSearchParams

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
    response_model=UserShow,
)
async def get_user(
        user: userDep
):
    return user



@user_router.get(
    "/@{username}/posts",
    summary="Получить посты пользователя",
    response_model=list[PostShow],
)
async def get_user_posts(
        user: userDep,
        service: postServiceDep,
        pagination: Pagination = Depends()
):
    return await service.get_user_posts(user=user, pagination=pagination)





@user_router.get(
    "/@{username}/top-topics",
    summary="Получить топ обсуждений",
    response_model=list[UserCommentsCountOfTopicShow],
)
async def get_top_topics(
        user: userDep,
        service: commentServiceDep,
):
    return await service.get_top_themes_of_user(user)





