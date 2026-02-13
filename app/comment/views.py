from fastapi import APIRouter, Depends

from auth.deps import currentUserDep, role_validate
from comment.deps import commentDep, commentServiceDep
from comment.schemas import CommentShow, CommentUpdate
from user.model import UserRoleEnum

comm_router = APIRouter(prefix="/comments", tags=["💬 Комментарии"])


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
        user: currentUserDep,
        comment: commentDep,
        service: commentServiceDep,
        comment_update: CommentUpdate,

):
    return await service.update_comment(
        comment=comment, comment_update=comment_update, user=user,
    )

@comm_router.delete(
    "/{comment_id}",
    summary="Удалить комментарий",
    dependencies=[Depends(role_validate(UserRoleEnum.MODERATOR))]
)
async def delete_comment(
    comment: commentDep,
    service: commentServiceDep,
):
    return await service.delete_item(comment)







