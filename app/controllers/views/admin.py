from base.db import getSessionDep
from deps.auth import currentUserDep

from fastapi import APIRouter, status, Query

from logic import  ProcessContainerAdminUseCase
from schemas.admin import AdminCreate


router = APIRouter(prefix="/admin", tags=["Админы"])


@router.post(
    "",
    summary="set admin",
    status_code=status.HTTP_201_CREATED
)
async def set_container_admin(
    session: getSessionDep,
    user: currentUserDep,
    admin: AdminCreate,
):
    logic =ProcessContainerAdminUseCase(session)

    return await logic.execute(
        user=user, admin=admin, method="create"
    )

@router.delete(
    "",
    summary="delete admin",
    status_code=status.HTTP_200_OK
)
async def delete_container_admin(
    session: getSessionDep,
    user: currentUserDep,
    admin: AdminCreate,
):
    logic = ProcessContainerAdminUseCase(session)

    return await logic.execute(
        user=user, admin=admin, method="delete"
    )

