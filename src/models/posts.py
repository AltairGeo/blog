from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from db.core import ModelBase
from schemas.tables import PostsSchema


class Posts(ModelBase): # Table for posts
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    text: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["Users"] = relationship(back_populates="posts")
    created_at: Mapped[datetime]

    def to_schema(self) -> PostsSchema:
        return PostsSchema(
            id=self.id,
            title=self.title,
            text=self.text,
            author_id=self.author_id,
            created_at=self.created_at,
        )
        
