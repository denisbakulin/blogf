from typing import Annotated

from allows.service import AllowService
from base.db import getSessionDep
from fastapi import Depends


async def get_comment_service(
        session: getSessionDep
) -> AllowService:
    return AllowService(session=session)


allowServiceDep = Annotated[AllowService, Depends(get_comment_service)]