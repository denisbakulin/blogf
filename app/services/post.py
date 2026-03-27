from base.service import BaseService
from entities import Post, User
from helpers.search import Pagination
from repositories import PostRepository
from schemas.post import PostCreate, PostUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from utils.post import generate_slug, add_metadata_to_slug


class PostService(BaseService[Post, PostRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Post, session, PostRepository)



    async def create_post(
            self, author_id: int,
            post: PostCreate,
            container_id: int
    ) -> Post:

        post = await self.create_item(
            **post.model_dump(),
            author_id=author_id,
            container_id=container_id
        )

        slug = generate_slug(post.title)

        ex_post = await self.repository.get_one_by(slug=slug)

        if ex_post is not None:
            slug = add_metadata_to_slug(slug, id=post.id)

        await self.update_item(post.id, slug=slug)

        return post



    # async def get_top_of_posts(self, q: str):
    #
    #     posts = await self.repository.get_top_of_topic_posts(q)
    #     return [TopPostShow(post=post, count=count) for post, count in posts]

    async def get_posts_with_authors(
            self, container_id: int,
            pagination: Pagination,
        ) -> list[tuple[Post, User]]:
        return await self.repository.get_container_posts(
            container_id=container_id,
            **pagination.dict()
        )


    async def update_post(self, post_id: int, update: PostUpdate) -> Post:
        return await self.update_item(post_id, **update.dict())

