from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import get_session
from comment.service import CommentService
from typing import Annotated


async def get_comment_service(
        session: AsyncSession = Depends(get_session)
) -> CommentService:
    return CommentService(session=session)


commentServiceDep = Annotated[CommentService, Depends(get_comment_service)]