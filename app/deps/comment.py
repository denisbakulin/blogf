from typing import Annotated
from base.db import getSessionDep
from fastapi import Depends
from services.comment import CommentService


async def get_comment_service(
        session: getSessionDep
) -> CommentService:
    return CommentService(session=session)


commentServiceDep = Annotated[CommentService, Depends(get_comment_service)]
