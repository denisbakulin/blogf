from fastapi import APIRouter

from auth.dependencies import verifiedUserDep
from comment.dependencies import commentDep, commentServiceDep
from comment.schemas import CommentShow, CommentUpdate

comm_router = APIRouter(prefix="/comments", tags=["comment"])


@comm_router.get(
    "/{comment_id}",
    response_model=CommentShow,
    summary="Получить комментарий по id"
)
async def get_comment(
        comment: commentDep
):
    return comment


@comm_router.patch(
    "/{comment_id}",
    response_model=CommentShow,
    summary="Изменить комментарий"
)
async def update_comment(
        comment: commentDep,
        user: verifiedUserDep,
        update_info: CommentUpdate,
        comment_service: commentServiceDep,
):
    return await comment_service.update_comment(comment, user, update_info)






