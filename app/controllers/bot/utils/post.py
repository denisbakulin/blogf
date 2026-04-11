from schemas.post import PostCreate
from pydantic import TypeAdapter

def ensure_correct_title(title: str):
    TypeAdapter(PostCreate.model_fields['title'].annotation).validate_python(title)

def ensure_correct_content(content: str):
    TypeAdapter(PostCreate.model_fields['content'].annotation).validate_python(content)