from schemas.base import BaseSchema
from datetime import datetime

class CreatePost(BaseSchema):
    title: str
    text: str
    # created_at: datetime = datetime.now(timezone.utc)
    token: str

class PostToClient(BaseSchema):
    id: int
    title: str
    text: str
    created_at: datetime = datetime.now()
    author_id: int
    author_name: str