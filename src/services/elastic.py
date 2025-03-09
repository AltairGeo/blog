from repositories.base import AbstractElasticRepo
from schemas.posts import FullPost
from elasticsearch import AsyncElasticsearch
from repositories.elastic import ElasticRepo
from typing import Dict, Any


class ElasticService:
    def __init__(self, elastic_repo: AbstractElasticRepo):
        self.elastic_repo = elastic_repo

    async def AddPostToIndex(self, post: FullPost):
        return await self.elastic_repo.add_to_index(doc_id=post.id, document=post.to_elastic())

    async def SearchPost(self, query: str, sort: Dict[str, Any], page: int):
        el_query = {
            "multi_match": {
                "query": query,
                "fields": ["title", "text", "author"],
            }
        }
        return await self.elastic_repo.search_in_index(query=el_query, sort=sort, page=page)





Service = ElasticService(
    elastic_repo=ElasticRepo(
        es_client=AsyncElasticsearch(
            "https://127.0.0.1:9200/",
            basic_auth=("elastic", "Nn2QHL8lLtO0sl7xBtZ0"),
            verify_certs=False
        ),
        index_name="posts"
    )
)

