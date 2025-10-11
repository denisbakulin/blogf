from typing import Annotated

from fastapi import Depends

from core.db import getSessionDep
from post.model import Post
from post.service import PostService


def get_post_service(
        session: getSessionDep
) -> PostService:
    return PostService(session=session)


postServiceDep = Annotated[PostService, Depends(get_post_service)]

async def get_post(
        slug: str,
        post_service: postServiceDep,
) -> Post:
    return await post_service.get_item_by(slug=slug)

postDep = Annotated[Post, Depends(get_post)]



