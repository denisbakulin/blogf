from fastapi import APIRouter
from comment.schemas import CommentShow, CommentUpdate
from comment.dependencies import commentServiceDep, commentDep
from auth.dependencies import verifiedUserDep


comm_router = APIRouter(prefix="/comments", tags=["comment"])


@comm_router.get("/{comment_id}", response_model=CommentShow)
async def get_comment(
        comment: commentDep
):
    return comment


@comm_router.patch(
    "/{comment_id}",
    response_model=CommentShow
)
async def update_comment(
        comment: commentDep,
        user: verifiedUserDep,
        update_info: CommentUpdate,
        comment_service: commentServiceDep,
):
    return await comment_service.update_comment(comment, user, update_info)






