from typing import Annotated

from base.db import getSessionDep
from deps.subscribe import SubscribeService
from fastapi import Depends
from entities.post import Post
from services.post import PostService

from deps.container import containerServiceDep
from usecases.post import GetPostUseCase

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



async def get_post_logic(
        post_service: postServiceDep,
        sub_service: SubscribeService,
        container_service: containerServiceDep
) -> GetPostUseCase:

    return GetPostUseCase(
        post_service=post_service,
        sub_service=sub_service,
        container_service=container_service
    )
