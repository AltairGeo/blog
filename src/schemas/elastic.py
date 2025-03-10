from typing import List

from schemas.base import BaseSchema
from schemas.posts import FullPost


class SearchResult(BaseSchema):
    total: int
    posts: List[FullPost]
