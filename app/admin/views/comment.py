from admin.views.base import AdminView
from comment.model import Comment
from comment.schemas import CommentShow


class CommentAdminView(AdminView, model=Comment, delete_=True):
    show = CommentShow

