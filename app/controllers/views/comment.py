from base.db import getSessionDep
from deps.auth import currentUserDep
from fastapi import APIRouter
from schemas.comment import CommentUpdate, CommentShow, UserUsername, CommentFullShow
from usecases.comment import DeleteCommentUseCase, UpdateCommentUseCase, GetCommentUseCase

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


@comm_router.get(
    "/{comment_id}",
    summary="Получить комментарий",
    response_model=CommentFullShow
)
async def get_comment(
        comment_id: int,
        user: currentUserDep,
        session: getSessionDep
):
    logic = GetCommentUseCase(session)

    comment, author, post = await logic.execute(user=user, comment_id=comment_id)

    return CommentFullShow(
        **CommentShow.from_orm(comment).model_dump(),
        author=UserUsername.from_orm(user),
        post_slug=post.slug
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



