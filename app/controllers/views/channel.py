from logic import UpdateContainerUseCase, GetChannelUseCase

from base.db import getSessionDep
from deps.auth import currentUserDep

from fastapi import APIRouter, status

from schemas.channel import CreatePublic, CreatePrivate
from schemas.container import ContainerShow, ContainerUpdate

from services.channel import PublicChannelService, PrivateChannelService
from services.subscribe import SubscribeService

router = APIRouter(prefix="/channels", tags=["Каналы "])




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
    sub = SubscribeService(session)

    channel = await service.create_private_channel(
        user_id=user.id, create=create
    )

    await sub.create_subscribe(user_id=user.id, container_id=channel.id)

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
    sub = SubscribeService(session)

    await sub.create_subscribe(user_id=user.id, container_id=channel.id)

    return ContainerShow.from_orm(channel)





@router.get(
    "/{channel_id}",
    summary="Посмотреть канал",
    response_model=ContainerShow
)
async def get_channel(
    channel_id: int,
    session: getSessionDep,
    user: currentUserDep
):
    logic = GetChannelUseCase(session)

    channel = await logic.execute(channel_id=channel_id, user=user)

    return ContainerShow.from_orm(channel)




@router.patch(
    "/{channel_id}",
    summary="Изменить канал",
)
async def update_channel(
    channel_id: int,
    update: ContainerUpdate,
    session: getSessionDep,
    user: currentUserDep
):
    logic = UpdateContainerUseCase(session)

    return await logic.execute(
        user=user, container_id=channel_id, update=update
    )
