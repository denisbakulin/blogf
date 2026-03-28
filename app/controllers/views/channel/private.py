from base.db import getSessionDep
from deps.auth import currentUserDep

from fastapi import APIRouter

from logic import (
    CreateInviteLinkUseCase,
    GetJRSUseCase,
    ProcessJRSPUseCase,
    GetInviteLinksUseCase,
)

from schemas.join_request import JRSUserShow, JRShow
from schemas.user import UserUsername

router = APIRouter(prefix="/{channel_id}")



@router.post(
    "/invite-links",
    tags=["invite link"]
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
    "/invite-links",
    tags=["invite link"]
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
    tags=["Join Request"],
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
    summary="Обработать заявку",
    tags=["Join Request"]
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





