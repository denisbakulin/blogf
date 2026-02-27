from base.service import BaseService
from helpers.search import Pagination
from models.post import Post
from repositories.post import PostRepository
from schemas.post import PostCreate, PostUpdate, TopPostShow
from services.container import ContainerService
from sqlalchemy.ext.asyncio import AsyncSession
from user import User
from utils.post import generate_slug


class PostService(BaseService[Post, PostRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Post, session, PostRepository)
        self.container_service = ContainerService(session=session)


    async def create_post(self, author_id: int, post: PostCreate) -> Post:

        post = await self.create_item(
            **post.model_dump(),
            author_id=author_id
        )

        slug = generate_slug(post.title, post.id)

        await self.update_item(post, slug=slug)

        return post

    async def get_top_of_posts(self, q: str):

        posts = await self.repository.get_top_of_topic_posts(q)
        return [TopPostShow(post=post, count=count) for post, count in posts]


    async def update_post(self, post: Post, post_update: PostUpdate) -> Post:

        await self.update_item(post, **post_update.model_dump())

        return post

    async def get_user_posts(self, user: User, pagination: Pagination) -> list[Post]:
        return await self.get_items_by(
            author_id=user.id,
            container_id=None,
            pagination=pagination
        )
