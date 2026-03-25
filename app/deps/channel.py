from typing import Annotated

from base.db import getSessionDep
from deps.container import get_container
from entities import Container, ContainerType
from fastapi import Depends
from services.channel import PrivateChannelService, PublicChannelService

__all__ = (
    "privateChannelServiceDep",
    'publicChannelServiceDep',
    'channelDep',
    'privateChannelDep',
    'publicChannelDep',
)



def get_private_channel_service(
        session: getSessionDep
) -> PrivateChannelService:
    return PrivateChannelService(session=session)

def get_public_channel_service(
        session: getSessionDep
) -> PublicChannelService:
    return PublicChannelService(session=session)


privateChannelServiceDep = Annotated[PrivateChannelService, Depends(get_private_channel_service)]
publicChannelServiceDep = Annotated[PublicChannelService, Depends(get_public_channel_service)]


channelDep = Annotated[
    Container,
    Depends(get_container([
        ContainerType.PRIVATE_CHANEL,
        ContainerType.PUBLIC_CHANNEL]
    ))
]

privateChannelDep = Annotated[
    Container, Depends(get_container(ContainerType.PRIVATE_CHANEL))
]

publicChannelDep = Annotated[
    Container, Depends(get_container(ContainerType.PUBLIC_CHANNEL))
]


