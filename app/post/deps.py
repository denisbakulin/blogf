from typing import Annotated

from base.db import getSessionDep
from fastapi import Depends
from post.model import Post
from post.service import PostService
from sub.deps import SubscribeService

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


from post.logic import PostLogic
from container.deps import containerServiceDep
async def get_post_logic(
        post_service: postServiceDep,
        sub_service: SubscribeService,
        container_service: containerServiceDep
) -> PostLogic:
    return PostLogic(
        post_service=post_service,
        sub_service=sub_service,
        container_service=container_service
    )


postLogicDep = Annotated[PostLogic, Depends(get_post_logic)]