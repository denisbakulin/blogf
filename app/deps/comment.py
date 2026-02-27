from typing import Annotated

from base.db import getSessionDep
from fastapi import Depends
from models.comment import Comment
from services.comment import CommentService


async def get_comment_service(
        session: getSessionDep
) -> CommentService:
    return CommentService(session=session)


commentServiceDep = Annotated[CommentService, Depends(get_comment_service)]


async def get_comment(
        comment_id: int,
        comment_service: commentServiceDep
) -> Comment:
    return await comment_service.get_comment_by_id(comment_id)

commentDep = Annotated[Comment, Depends(get_comment)]
