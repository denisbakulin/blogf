
from deps.auth import currentUserDep
from deps.comment import commentServiceDep
from deps.post import postDep, postServiceDep
from deps.reaction import reactionServiceDep
from fastapi import APIRouter, Depends, status

from helpers.search import Pagination
from schemas.comment import CommentCreate, CommentShow
from schemas.post import PostCreate, PostShow, PostUpdate, TopPostShow
from schemas.reaction import PostReactionShow
from utils.post import PostSearchParams
from usecases.post import GetPostUseCase, CreatePostUseCase, UpdatePostUseCase
from base.db import getSessionDep
from usecases.comment import GetCommentsUseCase, CreateCommentUseCase
from entities.reaction import ReactionType

from entities.container import ContainerType


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
    "/{slug}",
    summary="Получить пост",
    response_model=PostShow,
)
async def get_post(
        session: getSessionDep,
        slug: str,
        user: currentUserDep,
):
    logic = GetPostUseCase(session)

    return await logic.execute(user=user, slug=slug)


@router.patch(
    "/{slug}",
    summary="Изменить информацию о посте",
    response_model=PostShow
)
async def update_post(
        session: getSessionDep,
        slug: str,
        user: currentUserDep,
        update: PostUpdate,

):
    logic = UpdatePostUseCase(session)

    return await logic.execute(
        slug=slug, update=update, user=user
    )



@router.post(
    "/{slug}/comments",
    summary="Создать комментарий под постом",
    status_code=status.HTTP_201_CREATED
)
async def create_comment(
        slug: str,
        user: currentUserDep,
        session: getSessionDep,
        create: CommentCreate,

):
    logic = CreateCommentUseCase(session)

    return await logic.execute(
        create=create, user=user, post_slug=slug
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
    "/{slug}/comments",
    summary="Получить комментарии под постом",
)
async def get_post_comments(
        slug: str,
        user: currentUserDep,
        session: getSessionDep,
        pagination: Pagination = Depends(),
):
    logic = GetCommentsUseCase(session)

    return await logic.execute(
        user=user, post_slug=slug, pagination=pagination
    )



@router.post(
    "/{slug}/reactions",
    summary="Оставить реакцию под постом",
    status_code=status.HTTP_201_CREATED
)
async def add_post_reaction(
        post: postDep,
        user: currentUserDep,
        service: reactionServiceDep,
        reaction: ReactionType | None = None,
):
    return await service.process_post_reaction(
        user_id=user.id, post_id=post.id, reaction=reaction
    )


@router.get(
    "/{slug}/reactions",
    summary="Получить реакции поста",
)
async def get_post_reactions(
        post: postDep,
        like_service: reactionServiceDep,
        pagination: Pagination = Depends(),
        reaction: ReactionType | None = None,
):
    return await like_service.get_post_reactions(
        post_id=post.id, reaction_type=reaction, pagination=pagination
    )



