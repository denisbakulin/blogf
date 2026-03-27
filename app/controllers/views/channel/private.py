from base.db import getSessionDep
from deps.auth import currentUserDep

from fastapi import APIRouter

from schemas.container import ContainerShow, ContainerUpdate
from logic import (
    GetPrivateChannelUseCase,
    CreateInviteLinkUseCase,
    UpdateContainerUseCase,
    GetJRSUseCase,
    ProcessJRSPUseCase,
    GetInviteLinksUseCase
)

from schemas.join_request import JRSUserShow, JRShow
from schemas.user import UserUsername

router = APIRouter(prefix="/{channel_id}", tags=["Private channel"])


@router.get(
    "",
    summary="Посмотреть канал",
    response_model=ContainerShow
)
async def get_channel(
    channel_id: int,
    session: getSessionDep,
    user: currentUserDep,
):
    logic = GetPrivateChannelUseCase(session)

    channel = await logic.execute(
        user=user, channel_id=channel_id
    )

    return ContainerShow.from_orm(channel)

@router.patch(
    "",
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


@router.post(
    "/invite-links"
)
async def create_invite_link(
    user: currentUserDep,
    channel_id: int,
    session: getSessionDep
):
    logic = CreateInviteLinkUseCase(session)

    link = await logic.execute(user=user, channel_id=channel_id)

    return link

@router.get(
    "/invite-links"
)
async def get_invite_links(
    user: currentUserDep,
    channel_id: int,
    session: getSessionDep
):
    logic = GetInviteLinksUseCase(session)

    links = await logic.execute(user=user, channel_id=channel_id)

    return links



@router.get(
    "/joins",
    summary="Получить заявки в канал",
    response_model=list[JRSUserShow]
)
async def get_jrs(
    channel_id: int,
    session: getSessionDep,
    user: currentUserDep,
):
    logic = GetJRSUseCase(session)

    jrs = await logic.execute(user=user, channel_id=channel_id)

    return [
        JRSUserShow(
            **JRShow.from_orm(jr).model_dump(),
            user=UserUsername.from_orm(user)
        ) for jr, user in jrs
    ]


@router.post(
    "/join-process/{jr_id}",
    summary="Обработать заявку"
)
async def process_jr(
    channel_id: int,
    session: getSessionDep,
    user: currentUserDep,
    jr_id: int,
    accept: bool
):

    logic = ProcessJRSPUseCase(session)

    processed = await logic.execute(
        channel_id=channel_id, user=user, jr_id=jr_id, accept=accept
    )





