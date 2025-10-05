from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache

from auth.deps import currentUserDep, verifiedUserDep
from comment.deps import commentServiceDep
from comment.schemas import CommentCreate, CommentShow
from helpers.search import Pagination
from post.deps import postDep, postServiceDep
from post.schemas import PostCreate, PostShow, PostUpdate, FullPostShow
from post.utils import PostSearchParams
from reaction.deps import reactionServiceDep
from reaction.schemas import ReactionShow
from reaction.types import PostReactionsGetParams, PostReactionsSetParams

post_router = APIRouter(prefix="/posts", tags=["post"])




@post_router.post(
    "",
    summary="Создать пост",
    response_model=PostShow,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
        post_info: PostCreate,
        user: verifiedUserDep,
        post_service: postServiceDep
):
    return await post_service.create_post(user, post_info)


@post_router.get(
    "/{slug}",
    summary="Получить пост",
    response_model=FullPostShow,

)
@cache(expire=60)
async def get_post(
        post: postDep,
        reaction_service: reactionServiceDep
):
    reactions = await reaction_service.get_post_reaction_count(post)
    return FullPostShow(post=post, reactions=reactions)

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
    return await post_service.search_posts(search=search, pagination=pagination)


@post_router.put(
    "/{slug}",
    summary="Изменить информацию о посте",
    response_model=PostShow
)
async def update_post(
        post: postDep,
        user: verifiedUserDep,
        update_info: PostUpdate,
        post_service: postServiceDep,
):

    return await post_service.update_post(post, user, update_info)


@post_router.post(
    "/{slug}/comments",
    summary="Создать комментарий под постом",
    response_model=CommentShow,
    status_code=status.HTTP_201_CREATED

)
async def create_comment(
        post: postDep,
        comment_info: CommentCreate,
        comment_service: commentServiceDep,
        user: verifiedUserDep
):
    return await comment_service.create_comment(
        comment_info,
        user=user,
        post=post
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
    return await comment_service.get_post_comments(post=post, pagination=pagination)




@post_router.post(
    "/{slug}/reactions",
    summary="Оставить реакцию под постом",
    response_model=ReactionShow,
    status_code=status.HTTP_201_CREATED

)
async def add_post_reaction(
        post: postDep,
        reaction: PostReactionsSetParams,
        user: currentUserDep,
        like_service: reactionServiceDep,
):
    return await like_service.add_reaction(user, post, reaction)


@post_router.get(
    "/{slug}/reactions",
    summary="Получить реакци поста",
    response_model=list[ReactionShow],

)
async def get_post_reactions(
        post: postDep,
        t: PostReactionsGetParams,
        like_service: reactionServiceDep,
        pagination: Pagination = Depends()
):
    return await like_service.get_post_reactions(post, t, pagination)



