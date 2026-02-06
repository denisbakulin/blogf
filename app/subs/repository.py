from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from base.repository import BaseRepository
from subs.model import Subscribe
from post.model import Post

class SubscribeRepository(BaseRepository[Subscribe]):

    def __init__(self, session: AsyncSession):
        super().__init__(Subscribe, session)

    async def get_creators_posts(self, ids: list[int], limit: int, offset: int):
        stmt = select(Post).where(Post.author_id.in_(ids)).limit(limit).offset(offset)
        return await self.session.scalars(stmt)

    async def get_topics_posts(self, ids: list[int], limit: int, offset: int):
        stmt = select(Post).where(Post.container_id.in_(ids)).limit(limit).offset(offset)
        return await self.session.scalars(stmt)

    async def get_mixed_posts(self, uids: list[int], tids: list[int],limit: int, offset: int):
        stmt = select(Post).where(or_(Post.author_id.in_(uids), Post.container_id.in_(tids))).limit(limit).offset(offset)
        return await self.session.scalars(stmt)