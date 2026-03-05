from t.reaction import ReactionsGetParams, ReactionsSetParams
from typing import Literal

from deps.auth import currentUserDep
from deps.comment import commentServiceDep
from deps.post import postDep, postLogicDep, postServiceDep
from deps.reaction import reactionServiceDep
from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache
from helpers.search import Pagination
from schemas.comment import CommentCreate, CommentShow
from schemas.post import PostCreate, PostShow, PostUpdate, TopPostShow
from schemas.reaction import PostReactionShow
from utils.post import PostSearchParams

post_router = APIRouter(prefix="/posts", tags=["📝 Посты"])



@post_router.post(
    "",
    summary="Создать пост",
    response_model=PostShow
)
async def create_post(
        logic: postLogicDep,
        post: PostCreate,
        user: currentUserDep,
):
    return await logic.create_post(user=user, post=post)


@post_router.get(
    "/top",
    summary="Получить топ постов",
    response_model=list[TopPostShow],
)
async def get_top_of_posts(
        service: postServiceDep,
):
    return await service.get_top_of_topic_posts()





@post_router.get(
    "/search",
    summary="Поиск поста по ключевым параметрам",
    response_model=list[PostShow]
)
@cache(expire=120)
async def search_posts(
        post_service: postServiceDep,
        search: PostSearchParams = Depends(),
        pagination: Pagination = Depends()
):
    return await post_service.search_items(search=search, pagination=pagination)



@post_router.get(
    "/{slug}",
    summary="Получить пост",
    response_model=PostShow,

)
@cache(expire=60)
async def get_post(
        logic: postLogicDep,
        post: postDep,
        user: currentUserDep,
):

    return await logic.get_post(post=post, user=user)


@post_router.patch(
    "/{slug}",
    summary="Изменить информацию о посте",
    response_model=PostShow
)
async def update_post(
        logic: postLogicDep,
        post: postDep,
        user: currentUserDep,
        post_update: PostUpdate,

):
    return await logic.update_post(
        post=post, post_update=post_update, user=user
    )



@post_router.post(
    "/{slug}/comments",
    summary="Создать комментарий под постом",
    response_model=CommentShow,
    status_code=status.HTTP_201_CREATED
)
async def create_comment(
        post: postDep,
        comment_create: CommentCreate,
        comment_service: commentServiceDep,
        user: currentUserDep
):
    return await comment_service.create_comment(
        comment_create=comment_create, user=user, post=post
    )

@post_router.post(
    "/{slug}/as-anon/comments",
    summary="Создать комментарий анонимно",
    response_model=CommentShow,
    status_code=status.HTTP_201_CREATED
)
async def create_comment_as_anon(
        post: postDep,
        anon: anonDep,
        comment_create: CommentCreate,
        comment_service: commentServiceDep,

):
    return await comment_service.create_comment(
        comment_create=comment_create, user=anon, post=post
    )




@post_router.get(
    "/{slug}/comments",
    summary="Получить комментарии под постом",
    response_model=list[CommentShow],

)
async def get_post_comments(
        post: postDep,
        comment_service: commentServiceDep,
        pagination: Pagination = Depends(),
):
    return await comment_service.get_post_comments(
        post_id=post.id, pagination=pagination
    )




@post_router.post(
    "/{slug}/reactions",
    summary="Оставить реакцию под постом",
    response_model=PostReactionShow,
    status_code=status.HTTP_201_CREATED
)
async def add_post_reaction(
        post: postDep,
        reaction: ReactionsSetParams,
        user: currentUserDep,
        like_service: reactionServiceDep,
):
    return await like_service.process_post_reaction(
        user=user, post=post, reaction=reaction
    )


@post_router.get(
    "/{slug}/reactions",
    summary="Получить реакции поста",
    response_model=list[PostReactionShow],
)
async def get_post_reactions(
        post: postDep,
        type: ReactionsGetParams,
        like_service: reactionServiceDep,
        pagination: Pagination = Depends()
):
    return await like_service.get_post_reactions(
        post=post, reaction_type=type, pagination=pagination
    )



