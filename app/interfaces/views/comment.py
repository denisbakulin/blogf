from deps.comment import commentServiceDep
from fastapi import APIRouter

from schemas.comment import CommentShow, CommentUpdate


comm_router = APIRouter(prefix="/comments", tags=["💬 Комментарии"])


@comm_router.get(
    "/{comment_id}",
    response_model=CommentShow,
    summary="Получить комментарий по id"
)
async def get_comment(
        comment_id: int,
        service: commentServiceDep
):
    return await service.get_comment_by_id(comment_id)


@comm_router.patch(
    "/{comment_id}",
    response_model=CommentShow,
    summary="Изменить комментарий"
)
async def update_comment(
        comment: commentDep,
        service: commentServiceDep,
        update: CommentUpdate,

):

    return await service.update_comment(
        comment=comment, update=update,
    )

@comm_router.delete(
    "/{comment_id}",
    summary="Удалить комментарий",
)
async def delete_comment(
    comment: commentDep,
    service: commentServiceDep,
):
    return await service.delete_item_by_id(comment.id)







