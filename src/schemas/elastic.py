from schemas.base import BaseSchema
from schemas.posts import FullPost
from typing import List


class SearchResult(BaseSchema):
    total: int
    posts: List[FullPost]