from base.db import getSessionDep
from deps.auth import currentUserDep

from fastapi import APIRouter, status, Query

from entities import ContainerType
from logic import get_container_by_identifier, SetContainerAdminUseCase
from schemas.admin import AdminCreate

router = APIRouter(prefix="/admin", tags=[])


@router.post(
    "",
    summary="set admin",
    status_code=status.HTTP_201_CREATED
)
async def set_channel_admin(
    session: getSessionDep,
    user: currentUserDep,
    admin: AdminCreate,
    identifier: str = Query(...),
    ctype: ContainerType = Query(...),

):
    container = await get_container_by_identifier(
        ContainerType(ctype.value), identifier, session
    )

    logic = SetContainerAdminUseCase(session)

    return await logic.execute(
        user=user, container=container, admin=admin
    )
