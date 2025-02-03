from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from db.core import ModelBase
from schemas.tables import UsersSchema
from posts import PostsModel

class UsersModel(ModelBase): # Users table
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(unique=True)
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