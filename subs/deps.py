from typing import Annotated

from fastapi import Depends

from core.db import getSessionDep
from subs.service import SubscribeService


def get_subs_service(
        session: getSessionDep
) -> SubscribeService:
    return SubscribeService(session=session)


subscribeServiceDep = Annotated[SubscribeService, Depends(get_subs_service)]


