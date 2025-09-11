from post.service import PostService
from core.db import get_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

def get_post_service(
        session: AsyncSession = Depends(get_session)
) -> PostService:
    return PostService(session=session)



postServiceDep = Annotated[PostService, Depends(get_post_service)]