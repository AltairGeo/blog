from datetime import datetime

from schemas.base import BaseSchema


class CreatePost(BaseSchema):
    title: str
    text: str
    # created_at: datetime = datetime.now(timezone.utc)
    token: str


class FullPost(BaseSchema):
    id: int
    title: str
    text: str
    created_at: datetime = datetime.now()
    author_id: int
    author_name: str

    def to_elastic(self) -> dict:
        return {
            "title": self.title,
            "text": self.text,
            "created_at": self.created_at.isoformat(),
            "author": self.author_name,
        }


class DeletePostSchema(BaseSchema):
    id: int
    token: str


class ChangePostSchema(BaseSchema):
    token: str
    post_id: int
    title: str
    text: str
