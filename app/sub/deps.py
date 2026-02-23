from typing import Annotated

from base.db import getSessionDep
from fastapi import Depends
from sub.service import SubscribeService


def get_subs_service(
        session: getSessionDep
) -> SubscribeService:
    return SubscribeService(session=session)


subscribeServiceDep = Annotated[SubscribeService, Depends(get_subs_service)]


