from base.db import getSessionDep
from deps.auth import currentUserDep
from fastapi import APIRouter
from schemas.comment import CommentUpdate
from usecases.comment import DeleteCommentUseCase, UpdateCommentUseCase

comm_router = APIRouter(prefix="/comments", tags=["💬 Комментарии"])


@comm_router.patch(
    "/{comment_id}",
    summary="Изменить комментарий"
)
async def update_comment(
        comment_id: int,
        update: CommentUpdate,
        user: currentUserDep,
        session: getSessionDep
):
    logic = UpdateCommentUseCase(session)

    return await logic.execute(
        comment_id=comment_id, update=update, user=user
    )


@comm_router.delete(
    "/{comment_id}",
    summary="Удалить комментарий",
)
async def delete_comment(
        comment_id: int,
        user: currentUserDep,
        session: getSessionDep
):
    logic = DeleteCommentUseCase(session)

    return await logic.execute(comment_id=comment_id, user=user)







