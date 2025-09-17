from fastapi import APIRouter, Depends, HTTPException
from post.schemas import PostCreate, PostShow
from post.dependencies import postServiceDep
from auth.dependencies import currentUserDep
from helpers.pagination import Pagination

post_router = APIRouter(prefix="/posts", tags=["post"])


@post_router.post(
    "",
    response_model=PostShow
)
async def create_post(
        post_info: PostCreate,
        user: currentUserDep,
        post_service: postServiceDep
):
    return await post_service.create_post(user.id, post_info)



@post_router.get(
    "/by-slug/{slug}",
    response_model=list[PostShow]
)
async def get_posts_by_slug(
        slug: str,
        post_service: postServiceDep,
        pagination: Pagination = Depends(),

):
    return await post_service.get_posts_by_slug(slug, pagination.offset, pagination.limit)



@post_router.get(
    "/{post_id}",
    response_model=PostShow
)
async def get_post_by_id(
        post_id: int,
        post_service: postServiceDep
):
    return await post_service.get_post_by_id(post_id)





