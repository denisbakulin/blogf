
from base.db import getSessionDep
from deps.auth import currentUserDep
from deps.post import postDep, postServiceDep
from deps.reaction import reactionServiceDep
from entities import ContainerType, ReactionType
from fastapi import APIRouter, Depends, status
from helpers.search import Pagination
from schemas.comment import CommentCreate, CommentAuthorShow, CommentShow, UserUsername
from schemas.post import PostShow, PostUpdate, PostContainerShow, ContainerShow
from usecases.comment import CreateCommentUseCase, GetPostCommentsUseCase
from usecases.post import GetPostUseCase, UpdatePostUseCase, DeletePostUseCase
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
    "/{slug}",
    summary="Получить пост",
    response_model=PostContainerShow,
)
async def get_post(
        slug: str,
        session: getSessionDep,
        user: currentUserDep,
):
    logic = GetPostUseCase(session)

    post, container = await logic.execute(user=user, slug=slug)

    return PostContainerShow(
        **PostShow.from_orm(post).model_dump(),
        container=ContainerShow.from_orm(container)
    )

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


@router.delete(
    "/{slug}",
    summary="Удалить пост",
)
async def delete_post(
        session: getSessionDep,
        slug: str,
        user: currentUserDep,
):
    logic = DeletePostUseCase(session)

    return await logic.execute(
        slug=slug,  user=user
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
    response_model=list[CommentAuthorShow]
)
async def get_post_comments(
        slug: str,
        user: currentUserDep,
        session: getSessionDep,
        pagination: Pagination = Depends(),
):
    logic = GetPostCommentsUseCase(session)


    comments = await logic.execute(
        user=user, post_slug=slug, pagination=pagination
    )

    return [
        CommentAuthorShow(
            **CommentShow.from_orm(comment).model_dump(),
            author=UserUsername.from_orm(author)
        ) for comment, author, _ in comments
    ]


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
    await service.process_post_reaction(
        user_id=user.id, post_id=post.id, reaction=reaction
    )


@router.get(
    "/{slug}/reactions",
    summary="Получить реакции поста",
    response_model=list[ReactionAuthorShow]
)
async def get_post_reactions(
        post: postDep,
        service: reactionServiceDep,
        pagination: Pagination = Depends(),
        reaction: ReactionType | None = None,
):
    reactions = await service.get_post_reactions(
        post_id=post.id, reaction_type=reaction, pagination=pagination
    )

    return [
        ReactionAuthorShow(
            **ReactionShow.from_orm(reaction).model_dump(),
            author=UserUsername.from_orm(author)
        ) for reaction, author in reactions
    ]



