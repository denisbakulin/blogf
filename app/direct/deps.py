from typing import Annotated

from base.db import getSessionDep
from direct.service import DirectChatService
from fastapi import Depends


def get_direct_chat_service(
        session: getSessionDep
) -> DirectChatService:
    return DirectChatService(session=session)


directChatServiceDep = Annotated[DirectChatService, Depends(get_direct_chat_service)]




