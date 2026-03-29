
from base.db import getSessionDep
from deps.auth import currentUserDep
from deps.post import postDep, postServiceDep

from entities import ContainerType, ReactionType
from fastapi import APIRouter, Depends, status
from helpers.search import Pagination
from schemas.comment import CommentCreate, CommentAuthorShow, CommentShow, UserUsername
from schemas.post import PostShow, PostUpdate, PostContainerShow, ContainerShow

from logic import (
    GetPostUseCase,
    UpdatePostUseCase,
    DeletePostUseCase,
    CreateCommentUseCase,
    GetPostCommentsUseCase,
    GetPostReactionsUseCase,
    ProcessPostReactionUseCase

)
from utils.post import PostSearchParams
from schemas.reaction import ReactionPostShow, ReactionAuthorShow, PostSlug, UserUsername, ReactionShow

router = APIRouter(prefix="/posts", tags=["📝 Посты"])


@router.get(
    "/top",
    summary="Получить топ постов",
)
async def get_top_of_posts(
        service: postServiceDep,
):
    return await service.repository.get_top_of_container_posts(
        container_type=ContainerType.TOPIC, reaction_type=ReactionType.LIKE
    )



@router.get(
    "/search",
    summary="Поиск поста по ключевым параметрам",
)
async def search_posts(
        post_service: postServiceDep,
        search: PostSearchParams = Depends(),
        pagination: Pagination = Depends()
):
    return await post_service.search_items(search=search, pagination=pagination)



@router.get(
    "/{post_id}",
    summary="Получить пост",
    response_model=PostContainerShow,
)
async def get_post(
        post_id: int,
        session: getSessionDep,
        user: currentUserDep,
):
    logic = GetPostUseCase(session)

    post, container = await logic.execute(user=user, post_id=post_id)

    return PostContainerShow(
        **PostShow.from_orm(post).model_dump(),
        container=ContainerShow.from_orm(container)
    )

@router.patch(
    "/{post_id}",
    summary="Изменить информацию о посте",
    response_model=PostShow
)
async def update_post(
        session: getSessionDep,
        post_id: int,
        user: currentUserDep,
        update: PostUpdate,
):
    logic = UpdatePostUseCase(session)

    return await logic.execute(
        post_id=post_id, update=update, user=user
    )


@router.delete(
    "/{post_id}",
    summary="Удалить пост",
)
async def delete_post(
        session: getSessionDep,
        post_id: int,
        user: currentUserDep,
):
    logic = DeletePostUseCase(session)

    return await logic.execute(
        post_id=post_id,  user=user
    )


@router.post(
    "/{post_id}/comments",
    summary="Создать комментарий под постом",
    status_code=status.HTTP_201_CREATED
)
async def create_comment(
        post_id: int,
        user: currentUserDep,
        session: getSessionDep,
        create: CommentCreate,

):
    logic = CreateCommentUseCase(session)

    return await logic.execute(
        create=create, user=user, post_id=post_id
    )

#
# @router.post(
#     "/{slug}/as-anon/comments",
#     summary="Создать комментарий анонимно",
#     response_model=CommentShow,
#     status_code=status.HTTP_201_CREATED
# )
# async def create_comment_as_anon(
#         post: postDep,
#         anon: anonDep,
#         comment_create: CommentCreate,
#         comment_service: commentServiceDep,
#
# ):
#     return await comment_service.create_comment(
#         comment_create=comment_create, user=anon, post=post
#     )




@router.get(
    "/{post_id}/comments",
    summary="Получить комментарии под постом",
    response_model=list[CommentAuthorShow]
)
async def get_post_comments(
        post_id: int,
        user: currentUserDep,
        session: getSessionDep,
        pagination: Pagination = Depends(),
):
    logic = GetPostCommentsUseCase(session)


    comments = await logic.execute(
        user=user, post_id=post_id, pagination=pagination
    )

    return [
        CommentAuthorShow(
            **CommentShow.from_orm(comment).model_dump(),
            author=UserUsername.from_orm(author)
        ) for comment, author, _ in comments
    ]



@router.get(
    "/{post_id}/reactions",
    summary="Получить реакции поста",
    response_model=list[ReactionAuthorShow]
)
async def get_post_reactions(
    post_id: int,
    session: getSessionDep,
    user: currentUserDep,
    pagination: Pagination = Depends(),
    type: ReactionType | None = None,
):
    logic = GetPostReactionsUseCase(session)

    reactions = await logic.execute(
        user=user, post_id=post_id, reaction_type=type, pagination=pagination
    )

    return [
        ReactionAuthorShow(
            **ReactionShow.from_orm(reaction).model_dump(),
            author=UserUsername.from_orm(author)
        ) for reaction, author in reactions
    ]

@router.post(
    "/{post_id}/reactions",
    summary="Оставить реакцию под постом",
)
async def process_reaction(
    post_id: int,
    user: currentUserDep,
    session: getSessionDep,
    type: ReactionType | None = None,
):
    logic = ProcessPostReactionUseCase(session)

    await logic.execute(
        user=user, post_id=post_id, type=type
    )

