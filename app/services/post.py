from base.service import BaseService
from helpers.search import Pagination
from models.post import Post
from repositories.post import PostRepository
from schemas.post import PostCreate, PostUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from utils.post import generate_slug
from DTO.post import PostDTO

class PostService(BaseService[Post, PostRepository, PostDTO]):

    def __init__(self, session: AsyncSession):
        super().__init__(Post, session, PostRepository)



    async def create_post(self, author_id: int, post: PostCreate) -> PostDTO:

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


    async def update_post(self, post: PostDTO, update: PostUpdate) -> PostDTO:
        return await self.update_item(post.id, **update.model_dump())


    async def get_container_posts(self, container_id: int, pagination: Pagination) -> list[PostDTO]:
        return await self.repository.get_container_posts(
            container_id=container_id,
            **pagination.dict()
        )
