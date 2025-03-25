from datetime import datetime
from typing import List

from sqlalchemy import String, ForeignKey, Boolean, UniqueConstraint, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.expression import false

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
    likes: Mapped[List["PostsLikesModel"]] = relationship(
        "PostsLikesModel", back_populates="post", cascade="all, delete-orphan"
    )
    public: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def to_schema(self) -> PostsSchema:
        return PostsSchema(
            id=self.id,
            title=self.title,
            text=self.text,
            author_id=self.author_id,
            created_at=self.created_at,
            public=self.public,
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
            role=self.role,
            bio=self.bio,
        )


class PostsLikesModel(ModelBase):
    __tablename__ = "posts_likes"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))
    is_like: Mapped[bool] = mapped_column(Boolean, nullable=False)
    post: Mapped["PostsModel"] = relationship(back_populates="likes")

    __table_args__ = (
        UniqueConstraint("user_id", "post_id", name="user_post_unique"),
        Index("idx_post_user", "post_id", "user_id")
    )