from typing import Annotated

from fastapi import APIRouter, Depends, BackgroundTasks

from api.depends import elastic_service
from schemas.elastic import SearchResult
from services.elastic import ElasticService

router = APIRouter(
    prefix="/search",
    tags=["Search", "Posts"]
)

ann_elastic_service = Annotated[ElasticService, Depends(elastic_service)]


@router.get('/reindex')
async def re_index(search_service: ann_elastic_service, background_tasks: BackgroundTasks):
    if await search_service.ping():
        background_tasks.add_task(search_service.reindexation_of_posts)
        return True
    else:
        return False

@router.get('/find')
async def search_post(query: str, page: int, search_service: ann_elastic_service) -> SearchResult:
     return await search_service.SearchPost(
        page=page,
        query=query,
        sort={"created_at": {"order": "desc"}}
    )
