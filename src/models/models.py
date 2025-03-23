from datetime import datetime
from typing import List

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.core import ModelBase
from schemas.tables import PostsSchema, UsersSchema


class PostsModel(ModelBase):  # Table for posts
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    text: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["UsersModel"] = relationship(back_populates="posts")
    created_at: Mapped[datetime]

    def to_schema(self) -> PostsSchema:
        return PostsSchema(
            id=self.id,
            title=self.title,
            text=self.text,
            author_id=self.author_id,
            created_at=self.created_at,
        )


class UsersModel(ModelBase):  # Users table
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(unique=True)
    bio: Mapped[str] = mapped_column(String(100), nullable=True, unique=False)
    password: Mapped[str]
    avatar_path: Mapped[str] = mapped_column(nullable=True)
    posts: Mapped[List["PostsModel"]] = relationship(back_populates="author")
    role: Mapped[str] = mapped_column(nullable=True, unique=False)

    def to_schema(self) -> UsersSchema:
        return UsersSchema(
            id=self.id,
            nickname=self.nickname,
            email=self.email,
            password=self.password,
            avatar_path=self.avatar_path,
            role=self.role
        )
