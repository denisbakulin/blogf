from entities import Allow, AllowAction
from base.model import DBEntity
from repositories import AllowRepository
from base.service import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from abac.exceptions import InsufficientAllows
from abac.data import Context

class AllowService(BaseService[Allow, AllowRepository]):
    def __init__(self, session: AsyncSession):
        super().__init__(Allow, session, AllowRepository)

    async def create_allow(
        self, user_id: int,
        action: AllowAction,
        entity: DBEntity,
        container_id: int | None = None,
        against: bool = False,
    ) -> Allow:

        allow = await self.repository.get_one_by(
            user_id=user_id, action=action,
            entity=entity, container_id=container_id
        )

        if allow is None:
            return await self.create_item(
                user_id=user_id, action=action,
                entity=entity, container_id=container_id,
                againist=against
            )

        return await self.update_item(item_id=allow.id, against=against)


    async def check_access(
        self,
        user_id: int,
        action: AllowAction,
        entity: DBEntity,
        container_id: int | None = None,
        against: bool = False,
        **_,
    ):
        """
        :param against: Определяет логику обработки.
            ``bool``: проверяет правило на существование
            ``None``: raise если allow.against = False

        :raise
            InsufficientAllows
        """

        allow = await self.repository.get_one_by(
            user_id=user_id, action=action,
            entity=entity, container_id=container_id,
        )

        if against == True:
            if allow and allow.against:
                raise InsufficientAllows()

        if against == False:
            if allow and not allow.against:
                return

        if against is None:
            if not allow:
                return
            if not allow.against:
                return

        raise InsufficientAllows()




