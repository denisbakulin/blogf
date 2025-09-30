from post.service import PostService
from fastapi import Depends
from typing import Annotated
from core.db import getSessionDep
from post.repository import PostRepository
from post.model import Post

def get_post_service(
        session: getSessionDep
) -> PostService:
    return PostService(session=session)


postServiceDep = Annotated[PostService, Depends(get_post_service)]

async def get_post(
        slug: str,
        post_service: postServiceDep,
) -> Post:
    return await post_service.get_post_by_slug(slug)

postDep = Annotated[Post, Depends(get_post)]



