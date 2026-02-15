from sqlalchemy.ext.asyncio import AsyncSession

from base.exceptions import EntityBadRequestError, InsufficientPermissionsError
from base.service import BaseService
from helpers.search import Pagination
from post.model import Post
from post.repository import PostRepository
from post.schemas import PostCreate, PostUpdate, PostAllows,TopPostShow
from post.utils import generate_slug
from user.model import User

from topic.release.service import TopicService
from container.service import ContainerService
from container.model import Container, ContainerType as ct
from allows.service import AllowPostService


class PostService(BaseService[Post, PostRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Post, session, PostRepository)
        self.topic_service = TopicService(session=session)
        self.container_service = ContainerService(session=session)
        self.allows = AllowPostService(session=session)


    async def _create_post(self, author_id: int, post_create: PostCreate, allows: PostAllows) -> Post:
        post = await self.create_item(
            **post_create.model_dump(),
            **allows.model_dump(),
            author_id=author_id
        )

        slug = generate_slug(post.title, post.id)

        await self.update_item(post, slug=slug)

        return post


    async def create_post_private_channel(
            self, user: User,
            post_create: PostCreate,
            allows: PostAllows,
            channel: Container
    ) -> Post:
        can_create = await self.allows.can_create_private(user=user, channel=channel)

        if not can_create:
            raise InsufficientPermissionsError()

        return await self._create_post(
            author_id=user.id, post_create=post_create, allows=allows
        )

    async def create_post_public_channel(
            self, user: User,
            post_create: PostCreate,
            allows: PostAllows,
            channel: Container
    ) -> Post:
        can_create = await self.allows.can_create_public(user=user, channel=channel)

        if not can_create:
            raise InsufficientPermissionsError()

        return await self._create_post(
            author_id=user.id, post_create=post_create, allows=allows
        )

    async def create_post(self, user: User, post_create: PostCreate, allows: PostAllows) -> Post:

        container = None

        if post_create.container_id:
            container = await self.container_service.get_item_by_id(post_create.container_id)

        can_create = await self.allows.can_create(user=user, container=container)

        if not can_create:
            raise InsufficientPermissionsError()

        if container is None or container.type == ct.topic:
            return await self._create_post(author_id=user.id, post_create=post_create, allows=allows)

        props = dict(user=user, post_create=post_create, allows=allows, channel=container)

        process_func = {
            ct.public_channel: self.create_post_public_channel(**props),
            ct.private_channel: self.create_post_private_channel(**props)
        }[container.type]

        return await process_func



    async def get_top_of_posts(self, q: str):

        posts = await self.repository.get_top_of_posts(q)
        return [TopPostShow(post=post, count=count) for post, count in posts]


    async def update_post(self, post: Post, post_update: PostUpdate, user: User, allows: PostAllows) -> Post:

        can_update = await self.allows.can_update(user=user, post=post)
        if not can_update:
            raise EntityBadRequestError(
                "Post",
                f"Пост id={post.id} не принадлежит user={user.username}"
            )

        if allows is None:
            await self.update_item(post, **post_update.model_dump())
        else:
            await self.update_item(post, **post_update.model_dump(), **allows.model_dump(exclude_none=True))

        return post

    async def get_user_posts(self, user: User, pagination: Pagination) -> list[Post]:
        return await self.get_items_by(
            author_id=user.id,
            container_id=None,
            pagination=pagination
        )

