from deps.comment import commentDep, commentServiceDep
from fastapi import APIRouter
from schemas.comment import CommentUpdate

comm_router = APIRouter(prefix="/comments", tags=["💬 Комментарии"])



# @comm_router.get(
#     "/{comment_id}",
#     summary="Получить комментарий по id"
# )
# async def get_comment(
#         comment: commentDep
# ):
#     return comment


@comm_router.patch(
    "/{comment_id}",
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
    service: commentServiceDep,
    comment: commentDep,
):
    return await service.delete_item_by_id(comment.id)







