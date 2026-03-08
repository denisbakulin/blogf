from sqlalchemy.ext.asyncio import AsyncSession

from base.service import BaseService
from entities.post import Post
from helpers.search import Pagination
from repositories.post import PostRepository
from schemas.post import PostCreate, PostUpdate
from utils.post import generate_slug


class PostService(BaseService[Post, PostRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Post, session, PostRepository)



    async def create_post(self, author_id: int, post: PostCreate) -> Post:

        post = await self.create_item(
            **post.model_dump(),
            author_id=author_id
        )

        slug = generate_slug(post.title, post.id)

        await self.update_item(post.id, slug=slug)

        return post



    # async def get_top_of_posts(self, q: str):
    #
    #     posts = await self.repository.get_top_of_topic_posts(q)
    #     return [TopPostShow(post=post, count=count) for post, count in posts]

    async def get_container_posts(
            self, container_id: int,
            pagination: Pagination,
        ) -> list[tuple[Post]]:
        return await self.repository.get_container_posts(
            container_id=container_id,
            **pagination.dict()
        )
