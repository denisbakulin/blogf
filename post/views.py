from fastapi import APIRouter, Depends, HTTPException
from post.schemas import PostCreate, PostShow
from post.service import PostService
from post.dependencies import get_post_service
from post.exceptions import PostNotFoundErr
from auth.dependencies import get_current_user
from user.models import User
from helpers.pagination import Pagination

post_router = APIRouter(prefix="/posts", tags=["post"])


@post_router.post("", response_model=PostShow)
async def create_post(
        post_info: PostCreate,
        user: User = Depends(get_current_user),
        post_service: PostService = Depends(get_post_service)
):
    return await post_service.create_post(user, post_info)



@post_router.get("/by-slug/{slug}", response_model=list[PostShow])
async def get_posts_by_title(
        title: str,
        pagination: Pagination = Depends(),
        post_service: PostService = Depends(get_post_service)
):
    try:

        posts = await post_service.get_posts_by_title(title, pagination.offset, pagination.limit)
        return posts
    except PostNotFoundErr as e:
        raise HTTPException(404, detail=str(e))


@post_router.get("/{post_id}", response_model=PostShow)
async def get_post_by_id(
        post_id: int,
        post_service: PostService = Depends(get_post_service)
):
    try:
        posts = await post_service.get_post_by_id(post_id)
        return posts
    except PostNotFoundErr as e:
        raise HTTPException(404, detail=str(e))





