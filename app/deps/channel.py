from typing import Annotated

from base.db import getSessionDep
from deps.container import get_container
from entities import Container, ContainerType
from fastapi import Depends
from services.channel import PrivateChannelService, PublicChannelService

__all__ = (
    "privateChannelServiceDep",
    'publicChannelServiceDep',
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




publicChannelDep = Annotated[
    Container, Depends(get_container(ContainerType.PUBLIC_CHANNEL))
]


