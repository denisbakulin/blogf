from fastapi import APIRouter, Depends, HTTPException
from user.schemas import UserShow
from user.dependencies import get_user_service
from user.service import UserService

from helpers.pagination import Pagination
from post.service import PostService
from post.dependencies import get_post_service

from post.schemas import PostShow
from fastapi import Query


user_router = APIRouter(prefix="/users", tags=["user"])


@user_router.get(
    "/search",
    response_model=list[UserShow]
)
async def search_users(
        q: str = Query(min_length=1),
        pagination: Pagination = Depends(),
        user_service: UserService = Depends(get_user_service)
):
    return await user_service.search_users(q, pagination.offset, pagination.limit)

from asyncio import sleep


@user_router.get(
    "/@{username}",
    response_model=UserShow
)
async def get_user(
        username: str,
        service: UserService = Depends(get_user_service)
):
    await sleep(1)
    return await service.get_user_by_username(username)



@user_router.get(
    "/@{username}/posts",
    response_model=list[PostShow]
)
async def get_user_posts(
        username: str,
        post_service: PostService = Depends(get_post_service),
        user_service: UserService = Depends(get_user_service),
        pagination: Pagination = Depends()
):

    user = await user_service.get_user_by_username(username)
    posts = await post_service.get_posts_by_author_id(
        author_id=user.id,
        offset=pagination.offset,
        limit=pagination.limit
    )
    return posts





