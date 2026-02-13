from typing import Annotated

from fastapi import Depends

from base.db import getSessionDep

from channel.service import ChannelService

from container.model import Container


def get_channel_service(
        session: getSessionDep
) -> ChannelService:
    return ChannelService(session=session)



channelServiceDep = Annotated[ChannelService, Depends(get_channel_service)]

async def get_channel(
        service: channelServiceDep,
        slug: str
):
    return await service.get_channel(slug)

channelDep = Annotated[Container, Depends(get_channel)]
