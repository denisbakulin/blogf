from allows.model import Allow, AllowAction, DBEntity
from allows.repository import AllowRepository
from base.service import BaseService
from sqlalchemy.ext.asyncio import AsyncSession


class AllowService(BaseService[Allow, AllowRepository]):
    def __init__(self, session: AsyncSession):
        super().__init__(Allow, session, AllowRepository)

    async def create_allow(
            self, user_id: int,
            action: AllowAction,
            entity: DBEntity,
            context: DBEntity | None = None,
            context_id: int | None = None,
    ) -> Allow:
        allow = await self.repository.get_one_by(
            user_id=user_id, action=action, entity=entity, context=context, context_id=context_id
        )

        if allow is None:
            allow = await self.create_item(
                user_id=user_id, action=action,
                entity=entity, context=context,
                context_id=context_id
            )

        return allow





