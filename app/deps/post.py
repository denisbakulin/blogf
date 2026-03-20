from typing import Annotated

from base.db import getSessionDep
from entities import Post
from fastapi import Depends
from services.post import PostService


def get_post_service(
        session: getSessionDep
) -> PostService:
    return PostService(session=session)


postServiceDep = Annotated[PostService, Depends(get_post_service)]


async def get_post(
        slug: str,
        post_service: postServiceDep,
) -> Post:
    return await post_service.get_by_or_raise(slug=slug)

postDep = Annotated[Post, Depends(get_post)]
