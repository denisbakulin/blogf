from fastapi import Depends, APIRouter, HTTPException, Response, Cookie, BackgroundTasks
from comment.schemas import CommentCreate
from comment.dependencies import commentServiceDep
from auth.dependencies import verifiedUserDep


comm_router = APIRouter(prefix="/comment", tags=["auth"])



@comm_router.post("")
async def create_comment(
        comment_info: CommentCreate,
        comment_service: commentServiceDep,
        user: verifiedUserDep
):
    try:
        return await comment_service.create_comment(
            comment_info,
            author_id=user.id,
            post_id=comment_info.post_id,
            parent_id=comment_info.parent_id
        )
    except:
        raise


