from base.exceptions import AppError

MIN_POST_TITLE_LENGTH = 3
MAX_POST_TITLE_LENGTH = 100

MIN_POST_CONTENT_LENGTH = 10
MAX_POST_CONTENT_LENGTH = 5000


def ensure_correct_title(title: str):
    if not (MIN_POST_TITLE_LENGTH <= len(title) <= MAX_POST_TITLE_LENGTH):
        raise AppError()

def ensure_correct_content(content: str):
    if not (MIN_POST_CONTENT_LENGTH <= len(content) <= MAX_POST_CONTENT_LENGTH):
        raise AppError()
