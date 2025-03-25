from datetime import datetime
from typing import Optional

from schemas.base import BaseSchema


class CreatePost(BaseSchema):
    title: str
    text: str
    # created_at: datetime = datetime.now(timezone.utc)


class FullPost(BaseSchema):
    id: int
    title: str
    text: str
    created_at: datetime = datetime.now()
    author_id: int
    author_name: str
    likes: Optional[int] = None
    dislikes: Optional[int] = None
    public: bool

    def to_elastic(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "text": self.text,
            "created_at": self.created_at.isoformat(),
            "author": self.author_name,
        }


class ElasticPostResult(BaseSchema):
    id: int
    title: str
    text: str
    created_at: datetime = datetime.now()
    author: str


class DeletePostSchema(BaseSchema):
    id: int


class ChangePostSchema(BaseSchema):
    title: str
    text: str
