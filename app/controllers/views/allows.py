from base.db import getSessionDep
from deps.auth import currentUserDep

from fastapi import APIRouter
from logic.allow import CreateContainerAllowUseCase, AllowService
from schemas.allow import AllowCreate


router = APIRouter(prefix="/allows", tags=["Права"])



@router.post(
    "",
    summary="добавить право пользователю"
)
async def give_allow_to_user(
    allow: AllowCreate,
    user: currentUserDep,
    session: getSessionDep
):
    logic = CreateContainerAllowUseCase(session)

    return await logic.execute(admin=user, allow=allow)

@router.get(
    "",
    summary="Получить права пользователя"
)
async def get_user_allows(
    user: currentUserDep,
    session: getSessionDep
):
    service = AllowService(session)

    return await service.get_items_by(user_id=user.id)

