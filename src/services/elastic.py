from typing import Dict, Any

from fastapi import HTTPException

from repositories.base import AbstractElasticRepo
from repositories.posts import PostsRepository
from schemas.elastic import SearchResult
from schemas.posts import FullPost


class ElasticService:
    def __init__(self, elastic_repo: AbstractElasticRepo, posts_repo: PostsRepository):
        self.elastic_repo: AbstractElasticRepo = elastic_repo
        self.posts_repo: PostsRepository = posts_repo()

    async def AddPostToIndex(self, post: FullPost) -> bool:
        return await self.elastic_repo.add_to_index(doc_id=post.id, document=post.to_elastic())

    async def AddPostToIndexById(self, post_id: int) -> bool:
        post = await self.posts_repo.get_full_post(post_id)
        full_post = FullPost(
            id=post.id,
            title=post.title,
            author_id=post.author_id,
            created_at=post.created_at,
            author_name=post.author.nickname,
            text=post.text
        )
        return await self.AddPostToIndex(full_post)

    async def SearchPost(self, query: str, sort: Dict[str, Any], page: int) -> SearchResult:
        el_query = {
            "multi_match": {
                "query": query,
                "fields": ["title", "text", "author_name"],
            }
        }
        result = await self.elastic_repo.search_in_index(query=el_query, sort=sort, page=page)
        if result['hits']['hits'] == []:
            raise HTTPException(404, detail="Not found!")

        final_result = SearchResult(
            total=result['hits']['total']['value'],
            posts=[i['_source'] for i in result['hits']['hits']]
        )
        return final_result

    async def remove_post(self, post_id: int) -> bool:
        return await self.elastic_repo.remove_from_index(post_id)

    async def update_post(self, post_id: int, update_fields: Dict[str, Any]) -> bool:
        return await self.elastic_repo.update_in_index(post_id, update_fields=update_fields)

    async def reindexation_of_posts(self):
        posts = await self.posts_repo.get_all_posts()
        return await self.elastic_repo.bulk_add_to_index(posts)

    async def ping(self) -> bool:
        return await self.elastic_repo.ping()
