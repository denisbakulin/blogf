from .public import router as public_router
from .private import router as private_router

from base.db import getSessionDep
from deps.auth import currentUserDep

from fastapi import APIRouter, status

from schemas.channel import CreatePublic, CreatePrivate
from schemas.container import ContainerShow

from services.channel import PublicChannelService, PrivateChannelService


router = APIRouter(prefix="/channels", tags=[])
router.include_router(private_router)
router.include_router(public_router)


@router.post(
    "/private",
    summary="Создать private канал",
    status_code=status.HTTP_201_CREATED,
    response_model=ContainerShow
)
async def create_private_channel(
    create: CreatePrivate,
    user: currentUserDep,
    session: getSessionDep
):
    service = PrivateChannelService(session)

    channel = await service.create_private_channel(
        user_id=user.id, create=create
    )

    return ContainerShow.from_orm(channel)


@router.post(
    "/public",
    summary="Создать public канал",
    status_code=status.HTTP_201_CREATED,
    response_model=ContainerShow
)
async def create_public_channel(
    create: CreatePublic,
    user: currentUserDep,
    session: getSessionDep
):
    service = PublicChannelService(session)

    channel = await service.create_public_channel(
        user_id=user.id, create=create
    )

    return ContainerShow.from_orm(channel)





