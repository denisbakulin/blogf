from typing import Annotated

from fastapi import Depends, Path

from base.db import getSessionDep
from entities.comment import Comment
from services.comment import CommentService


async def get_comment_service(
        session: getSessionDep
) -> CommentService:
    return CommentService(session=session)


commentServiceDep = Annotated[CommentService, Depends(get_comment_service)]


async def get_comment(
    service: commentServiceDep,
    comment_id: int = Path()
) -> Comment:
    return await service.get_comment_by_id(comment_id)

commentDep = Annotated[Comment, Depends(get_comment)]