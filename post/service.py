from sqlalchemy.ext.asyncio import AsyncSession
from post.repository import PostRepository
from post.schemas import PostCreate
from post.models import Post
from core.exceptions import EntityNotFoundError


class PostService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.post_repo = PostRepository(session)

    async def create_post(self, author_id: int, post_info: PostCreate) -> Post:

        post = self.post_repo.create_post(post_info.model_dump(), author_id=author_id)

        await self.session.commit()
        await self.session.refresh(post)

        return post

    async def _get_posts_by(
            self,
            offset: int,
            limit: int,
            **filters
    ):
        posts = await self.post_repo.get_posts(**filters, offset=offset, limit=limit)
        if not posts:
            raise EntityNotFoundError(
                "Post",
                fields=filters
            )
        return posts

    async def get_post_by_id(self, post_id: int) -> Post:
        post = await self.post_repo.get_post(post_id=post_id)

        if not post:
            raise EntityNotFoundError(
                "Post",
                entity_id=post_id
            )

        return post

    async def get_posts_by_title(
            self,
            title: str,
            offset: int,
            limit: int
    ) -> list[Post]:
        return await self._get_posts_by(offset=offset, limit=limit, title=title)

    async def get_posts_by_slug(
            self,
            slug: str,
            offset: int,
            limit: int
    ) -> list[Post]:
        return await self._get_posts_by(offset=offset, limit=limit, slug=slug)

    async def get_posts_by_author_id(
            self,
            author_id: int,
            offset: int,
            limit: int
    ) -> list[Post]:
        return await self._get_posts_by(offset=offset, limit=limit, author_id=author_id)