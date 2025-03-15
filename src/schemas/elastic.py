from typing import List

from schemas.base import BaseSchema
from schemas.posts import ElasticPostResult


class SearchResult(BaseSchema):
    total: int
    posts: List[ElasticPostResult]
