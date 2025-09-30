from fastapi import APIRouter, Depends
from post.schemas import PostCreate, PostShow, PostUpdate
from post.dependencies import postServiceDep, postDep
from auth.dependencies import verifiedUserDep
from helpers.search import Pagination

from comment.dependencies import commentServiceDep
from comment.schemas import CommentShow
from post.utils import PostSearchParams
from comment.schemas import CommentCreate

from auth.dependencies import currentUserDep

from reaction.schemas import ReactionShow
from reaction.dependencies import reactionServiceDep


post_router = APIRouter(prefix="/posts", tags=["post"])




@post_router.post(
    "",
    response_model=PostShow
)
async def create_post(
        post_info: PostCreate,
        user: verifiedUserDep,
        post_service: postServiceDep
):
    return await post_service.create_post(user.id, post_info)


@post_router.get(
    "/{slug}",
    response_model=PostShow
)
async def get_post(
        post: postDep
):
    return post


@post_router.get(
    "/search",
    response_model=list[PostShow]
)
async def search_posts(
        post_service: postServiceDep,
        search: PostSearchParams = Depends(),
        pagination: Pagination = Depends()

):
    return await post_service.search_posts(search=search, pagination=pagination)


@post_router.patch(
    "/{slug}",
    response_model=PostShow
)
async def update_post(
        post: postDep,
        user: verifiedUserDep,
        update_info: PostUpdate,
        post_service: postServiceDep,
):
    return await post_service.update_post(post, user, update_info)


@post_router.post("/{slug}/comments", response_model=CommentShow)
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
    response_model=list[CommentShow]
)
async def get_post_comments(
        post: postDep,
        comment_service: commentServiceDep,
        pagination: Pagination = Depends(),
):
    return await comment_service.get_post_comments(post=post, pagination=pagination)



from reaction.types import PostReactionsSetParams, PostReactionsGetParams

@post_router.post(
    "/{slug}/reactions",
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
    response_model=list[ReactionShow]
)
async def get_post_reactions(
        post: postDep,
        t: PostReactionsGetParams,
        like_service: reactionServiceDep,
        pagination: Pagination = Depends()
):
    return await like_service.get_post_reactions(post, t, pagination)



