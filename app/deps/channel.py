from typing import Annotated

from fastapi import Depends

from base.db import getSessionDep
from deps.container import get_container
from entities.container import Container, ContainerType
from services.channel import (ChannelService, PrivateChannelService,
                              PublicChannelService, channels)

__all__ = (
    "channelServiceDep",
    "privateChannelServiceDep",
    'publicChannelServiceDep',
    'channelDep' ,
    'privateChannelDep' ,
    'publicChannelDep' ,
)
def get_channel_service(
        session: getSessionDep
) -> ChannelService:
    return ChannelService(session=session)

def get_private_channel_service(
        session: getSessionDep
) -> PrivateChannelService:
    return PrivateChannelService(session=session)

def get_public_channel_service(
        session: getSessionDep
) -> PublicChannelService:
    return PublicChannelService(session=session)



channelServiceDep = Annotated[ChannelService, Depends(get_channel_service)]
privateChannelServiceDep = Annotated[PrivateChannelService, Depends(get_private_channel_service)]
publicChannelServiceDep = Annotated[PublicChannelService, Depends(get_public_channel_service)]


channelDep = Annotated[
    Container,
    Depends(get_container([
        ContainerType.private_channel,
        ContainerType.public_channel]
    ))
]

privateChannelDep = Annotated[
    Container, Depends(get_container(ContainerType.private_channel))
]

publicChannelDep = Annotated[
    Container, Depends(get_container(ContainerType.public_channel))
]


