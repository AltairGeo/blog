from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy import String, ForeignKey
from typing import List
from datetime import datetime

#  _____     _     _
# |_   _|_ _| |__ | | ___  ___
#   | |/ _` | '_ \| |/ _ \/ __|
#   | | (_| | |_) | |  __/\__ \
#   |_|\__,_|_.__/|_|\___||___/
#

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Users(Base): # Users table
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    avatar_path: Mapped[str] = mapped_column(nullable=True)
    posts: Mapped[List["Posts"]] = relationship(back_populates="author")
    role: Mapped[str] = mapped_column(nullable=True, unique=False)

class Posts(Base): # Table for posts
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    text: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["Users"] = relationship(back_populates="posts")
    created_at: Mapped[datetime]
