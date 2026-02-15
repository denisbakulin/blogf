from typing import Annotated

from fastapi import Depends

from base.db import getSessionDep

from allows.service import AllowService, AllowPostService


async def get_comment_service(
        session: getSessionDep
) -> AllowPostService:
    return AllowPostService(session=session)


allowServiceDep = Annotated[AllowPostService, Depends(get_comment_service)]