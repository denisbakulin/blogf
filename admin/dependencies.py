from admin.service import AdminService
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable
from core.db import getSessionDep

def get_admin_service(
        model,
) -> Callable[[AsyncSession], AdminService]:
    def wrapper(session: getSessionDep):
        return AdminService[model](model=model, session=session)
    return wrapper


