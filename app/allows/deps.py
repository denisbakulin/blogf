from typing import Annotated

from fastapi import Depends

from allows.service import AllowPostService, AllowService
from base.db import getSessionDep


async def get_comment_service(
        session: getSessionDep
) -> AllowPostService:
    return AllowPostService(session=session)


allowServiceDep = Annotated[AllowPostService, Depends(get_comment_service)]