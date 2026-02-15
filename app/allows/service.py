from base.service import BaseService
from allows.repository import AllowRepository
from allows.model import Allow, AllowAction, AllowEntity
from sqlalchemy.ext.asyncio import AsyncSession
from user.model import User
from sub.service import SubscribeService
from container.model import Container, ContainerType as ct
from post.model import Post

class AllowService(BaseService[Allow, AllowRepository]):
    def __init__(self, session: AsyncSession):
        super().__init__(Allow, session, AllowRepository)

    def get_sorted(self, allow_list: list[Allow], entity_type: AllowEntity):
        ...


    async def create_allow(
            self, user_id: int,
            action: AllowAction,
            entity: AllowEntity,
            context: AllowEntity | None = None,
            context_id: int | None = None,
            against: bool = False
    ) -> Allow:
        allow = await self.repository.get_one_by(
            user_id=user_id, action=action, entity=entity, context=context, context_id=context_id
        )

        if allow is None:
            allow = await self.create_item(user_id=user_id, action=action, entity=entity, context=context, context_id=context_id)

        return await self.update_item(allow, against=against)




def any_allows(allows: list) -> bool:
    ...

class AllowPostService(AllowService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.sub_service = SubscribeService(session)


    async def can_read_private(self, user: User, channel: Container):
        subscribes = await self.sub_service.repository.get_any_by(
            container_id=channel.id, lines=["user_id"]
        )

        return user.id in [*[i[0] for i in subscribes], channel.author_id]


    can_create_public = can_read_private

    async def can_create_private(self, user: User, channel: Container):
        can_read = await self.can_read_private(user=user, channel=channel)


        if not can_read:
            return False

        user_allows_create = await self.get_user_post_allows(
            user=user, container=channel, action=AllowAction.CREATE
        )

        can_create = next(
            (
                not allow.against for allow in
                (i for i in user_allows_create if i.context_id == channel.id)
            ), False
        )

        return can_create or user.id == channel.author_id



    async def get_user_post_allows(self, user: User, container: Container, action: AllowAction):
        return await self.repository.get_any_by(
            user_id=user.id, action=action,
            context=[None, AllowEntity.CONTAINER], entity=AllowEntity.POST,
            context_id=[None, container.id if container else None]
        )

    async def can_create(
            self, user: User,
            container: Container | None,
    ):
        user_allows = await self.get_user_post_allows(user=user, container=container, action=AllowAction.CREATE)

        glb_allow = next((not allow.against for allow in user_allows
                          if allow.context is None), True)

        if container is None:
            return glb_allow

        ctx_allow = next((not allow.against for allow in user_allows
                          if allow.context_id == container.id), True)

        for allow in [ctx_allow, glb_allow]:
            if allow:
                return True

        return False

    async def can_delete(self, user: User, post: Post):
        return user.id == post.author_id

    async def can_update(self, user: User, post: Post):
        if user.id == post.author_id:
            return True
        if post.container and user.id == post.container.author_id:
            return True

        return False


