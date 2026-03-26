from base.repository import BaseRepository
from entities import PinnedPost
from sqlalchemy.ext.asyncio import AsyncSession


class PinnedPostRepository(BaseRepository[PinnedPost]):

    def __init__(self, session: AsyncSession):
        super().__init__(PinnedPost, session)







