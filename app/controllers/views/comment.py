from base.db import getSessionDep
from deps.auth import currentUserDep
from fastapi import APIRouter, status, Depends

from helpers.search import Pagination

from schemas.comment import (
    CommentUpdate,
    CommentShow,
    UserUsername,
    CommentFullShow,
    CommentAuthorShow,
    CommentCreate
)

from logic import (
    DeleteCommentUseCase,
    UpdateCommentUseCase,
    GetCommentUseCase,
    GetPostCommentsUseCase,
    CreateCommentUseCase
)

from schemas.post import PostID
from services.comment import CommentService

router = APIRouter(prefix="/comments", tags=["💬 Комментарии"])


@router.patch(
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


@router.get(
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




@router.delete(
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




@router.post(
    "/posts",
    summary="Создать комментарий под постом",
    status_code=status.HTTP_201_CREATED
)
async def create_comment(
    post: PostID,
    user: currentUserDep,
    session: getSessionDep,
    create: CommentCreate,

):
    logic = CreateCommentUseCase(session)

    return await logic.execute(
        create=create, user=user, post_id=post.id
    )





@router.get(
    "/posts/{post_id}",
    summary="Получить комментарии под постом",
    response_model=list[CommentAuthorShow]
)
async def get_post_comments(
    post_id: int,
    user: currentUserDep,
    session: getSessionDep,
    pagination: Pagination = Depends(),
):
    logic = GetPostCommentsUseCase(session)


    comments = await logic.execute(
        user=user, post_id=post_id, pagination=pagination
    )

    return [
        CommentAuthorShow(
            **CommentShow.from_orm(comment).model_dump(),
            author=UserUsername.from_orm(author)
        ) for comment, author, _ in comments
    ]



@router.get(
    "/me",
    summary="Получить комментарии текущего пользователя",
    response_model=list[CommentFullShow]
)
async def get_my_comments(
    user: currentUserDep,
    session: getSessionDep,
    pagination: Pagination = Depends()
):

    service = CommentService(session)

    comments = await service.get_user_comments(
        user_id=user.id, pagination=pagination
    )

    return [
        CommentFullShow(
            **CommentShow.from_orm(comment).model_dump(),
            author_username=user.username,
            post_slug=post.slug,
        )
        for comment, user, post in comments
    ]


