from post.repository import PostRepository
from post.service import PostService
from core.db import get_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession


def get_post_repo(session: AsyncSession):
    return PostRepository(session=session)


def get_post_service(
        session: AsyncSession = Depends(get_session)
) -> PostService:
    return PostService(session=session)
