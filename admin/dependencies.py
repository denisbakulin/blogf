from admin.service import AdminService
from core.db import get_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable


def get_admin_service(
        model,
) -> Callable[[AsyncSession], AdminService]:
    def wrapper(session: AsyncSession = Depends(get_session)):
        return AdminService[model](model=model, session=session)
    return wrapper

