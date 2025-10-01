from fastapi import APIRouter, Depends

from helpers.search import Pagination
from post.dependencies import postServiceDep
from post.schemas import PostShow
from user.dependencies import userDep, userServiceDep
from user.schemas import UserShow
from user.utils import UserSearchParams

user_router = APIRouter(prefix="/users", tags=["user"])


@user_router.get(
    "/search",
    summary="Поиск пользователя по ключевым параметрам",
    response_model=list[UserShow],

)
async def search_users(
        user_service: userServiceDep,
        search: UserSearchParams = Depends(),
        pagination: Pagination = Depends(),
):
    return await user_service.search_users(search=search, pagination=pagination)


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
        post_service: postServiceDep,
        pagination: Pagination = Depends()
):
    posts = await post_service.get_posts_by_author_id(
        author_id=user.id,
        pagination=pagination
    )
    return posts







