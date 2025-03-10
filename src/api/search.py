from fastapi import APIRouter, Depends
from services.elastic import ElasticService
from api.depends import elastic_service
from typing import Annotated
from schemas.elastic import SearchResult

router = APIRouter(
    prefix="/search",
    tags=["Search", "Posts"]
)

ann_elastic_service = Annotated[ElasticService, Depends(elastic_service)]


@router.get('/reindex')
async def re_index(search_service: ann_elastic_service):
    return await search_service.reindexation_of_posts()

@router.get('/find')
async def search_post(query: str, page: int, search_service: ann_elastic_service) -> SearchResult:
    return await search_service.SearchPost(
        page=page,
        query=query,
        sort={"created_at": {"order": "desc"}}
    )
