from typing import Annotated

from fastapi import Depends

from base.db import getSessionDep

from channel.service import ChannelService

def get_channel_service(
        session: getSessionDep
) -> ChannelService:
    return ChannelService(session=session)


channelServiceDep = Annotated[ChannelService, Depends(get_channel_service)]



