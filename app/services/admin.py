from sqlalchemy.ext.asyncio import AsyncSession
from entities import Admin
from repositories import AdminRepository
from base.service import BaseService



class AdminService(BaseService[Admin, AdminRepository]):

    def __init__(self, session: AsyncSession):
        super().__init__(Admin, session, AdminRepository)


    async def create_admin(self, user_id: int, container_id: int):
        params = {'user_id': user_id, 'container_id': container_id}

        await self.create_if_not_exists(exists_spec=params, create=params)



