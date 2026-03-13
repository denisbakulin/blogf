from typing import Annotated

from base.db import getSessionDep
from fastapi import Depends
from services.container import Container, ContainerService, ContainerType


async def get_container_service(
    session: getSessionDep
) -> ContainerService:
    return ContainerService(session=session)

containerServiceDep = Annotated[ContainerService, Depends(get_container_service)]


def get_container(type_: ContainerType | list[ContainerType]):
    async def wrapper(
            service: containerServiceDep,
            slug: str
    ) -> Container:
        return await service.get_by_or_raise(slug=slug, type=type_)

    return wrapper


