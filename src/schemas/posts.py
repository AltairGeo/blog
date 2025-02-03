from schemas.base import BaseSchema

class CreatePost(BaseSchema):
    title: str
    text: str
    # created_at: datetime = datetime.now(timezone.utc)
    token: str