from typing import Annotated

from base.db import getSessionDep
from fastapi import Depends
from services.container import ContainerService


async def get_container_service(
    session: getSessionDep
) -> ContainerService:
    return ContainerService(session=session)

containerServiceDep = Annotated[ContainerService, Depends(get_container_service)]



