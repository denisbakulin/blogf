from base.db import getSessionDep
from deps.auth import currentUserDep

from entities import ReactionType
from fastapi import APIRouter, Depends
from helpers.search import Pagination

from logic import (
    GetPostReactionsUseCase,
    ProcessPostReactionUseCase,
)

from schemas.reaction import ReactionAuthorShow, UserUsername, ReactionShow, ReactionPostShow
from schemas.post import PostID, PostSlug
from services.reaction import ReactionService

router = APIRouter(prefix="/reactions", tags=["❤️ Реакции"])



@router.get(
    "/posts",
    summary="Получить реакции поста",
    response_model=list[ReactionAuthorShow]
)
async def get_post_reactions(
    post: PostID,
    session: getSessionDep,
    user: currentUserDep,
    pagination: Pagination = Depends(),
    type: ReactionType | None = None,
):
    logic = GetPostReactionsUseCase(session)

    reactions = await logic.execute(
        user=user, post_id=post.id, reaction_type=type, pagination=pagination
    )

    return [
        ReactionAuthorShow(
            **ReactionShow.from_orm(reaction).model_dump(),
            author=UserUsername.from_orm(author)
        ) for reaction, author in reactions
    ]

@router.post(
    "/posts",
    summary="Оставить реакцию под постом",
)
async def process_reaction(
    post: PostID,
    user: currentUserDep,
    session: getSessionDep,
    type: ReactionType | None = None,
):
    logic = ProcessPostReactionUseCase(session)

    await logic.execute(
        user=user, post_id=post.id, type=type
    )




@router.get(
    "/posts",
    summary="Получить реакции поста",
    response_model=list[ReactionAuthorShow]
)
async def get_post_reactions(
    post: PostID,
    session: getSessionDep,
    user: currentUserDep,
    pagination: Pagination = Depends(),
    type: ReactionType | None = None,
):
    logic = GetPostReactionsUseCase(session)

    reactions = await logic.execute(
        user=user, post_id=post.id, reaction_type=type, pagination=pagination
    )

    return [
        ReactionAuthorShow(
            **ReactionShow.from_orm(reaction).model_dump(),
            author=UserUsername.from_orm(author)
        ) for reaction, author in reactions
    ]


@router.get(
    "/me",
    summary="Получить реакции пользователя",
    response_model=list[ReactionPostShow]
)
async def get_my_reactions(
    user: currentUserDep,
    session: getSessionDep,
    type: ReactionType | None = None,
    pagination: Pagination = Depends()
):

    service = ReactionService(session)

    reactions = await service.get_user_reactions(
        user_id=user.id, reaction_type=type, pagination=pagination
    )

    return [
        ReactionPostShow(
            **ReactionShow.from_orm(reaction).model_dump(),
            post=PostSlug.from_orm(post)
        )
        for reaction, post in reactions
    ]







