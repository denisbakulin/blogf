from fastapi import APIRouter
from base.db import getSessionDep
from deps.auth import currentUserDep

from logic import CrossToInviteLinkUseCase, DeleteInviteLinkUseCase, GetInviteLinksUseCase, CreateInviteLinkUseCase
from schemas.link import DeleteLink
from schemas.channel import ChannelID

router = APIRouter(prefix="/invite-links", tags=["Вступительная ссылки"])


@router.post(
    "/process/{link}",
    summary="Перейти по вступительной ссылке",
)
async def process_invite_link(
    link: str,
    user: currentUserDep,
    session: getSessionDep
):
    logic = CrossToInviteLinkUseCase(session)

    return await logic.execute(link=link, user=user)



@router.post(
    "",
    summary="Создать вступительную ссылку",
)
async def create_invite_link(
    user: currentUserDep,
    channel: ChannelID,
    session: getSessionDep
):
    logic = CreateInviteLinkUseCase(session)

    link = await logic.execute(user=user, channel_id=channel.id)

    return link

@router.get(
    "",
    summary="Получить ссылки",
)
async def get_invite_links(
    user: currentUserDep,
    channel_id: int,
    session: getSessionDep
):
    logic = GetInviteLinksUseCase(session)

    links = await logic.execute(user=user, channel_id=channel_id)

    return links

@router.delete(
    "",
    summary="Удалить ссылку",
)
async def delete_invite_link(
    link: DeleteLink,
    channel: ChannelID,
    user: currentUserDep,
    session: getSessionDep
):
    logic = DeleteInviteLinkUseCase(session)

    await logic.execute(link=link, user=user, channel_id=channel.id)
