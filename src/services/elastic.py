from repositories.base import AbstractElasticRepo
from schemas.posts import FullPost
from repositories.posts import PostsRepository
from typing import Dict, Any, List
from fastapi import HTTPException


class ElasticService:
    def __init__(self, elastic_repo: AbstractElasticRepo, posts_repo: PostsRepository):
        self.elastic_repo: AbstractElasticRepo = elastic_repo
        self.posts_repo: PostsRepository = posts_repo()

    async def AddPostToIndex(self, post: FullPost):
        return await self.elastic_repo.add_to_index(doc_id=post.id, document=post.to_elastic())

    async def SearchPost(self, query: str, sort: Dict[str, Any], page: int) -> Dict[str, Any]:
        el_query = {
            "multi_match": {
                "query": query,
                "fields": ["title", "text", "author"],
            }
        }
        result = await self.elastic_repo.search_in_index(query=el_query, sort=sort, page=page)
        if result['hits']['hits'] == []:
            raise HTTPException(404, detail="Not found!")

        pretty = {
                "total": result['hits']['total']['value'],
                "posts": result['hits']['hits']
        }
        return pretty


    async def RemovePost(self, post_id: int) -> bool:
        return await self.elastic_repo.remove_from_index(post_id)


    async def UpdatePost(self, post_id: int, update_fields: Dict[str, Any]) -> bool:
        return await self.elastic_repo.update_in_index(post_id, update_fields=update_fields)


    async def ReIndex(self):
        posts = await self.posts_repo.get_all_posts()
        return await self.elastic_repo.bulk_add_to_index(posts)