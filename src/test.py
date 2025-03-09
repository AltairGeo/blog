from services.elastic import Service
from datetime import datetime
from schemas.posts import FullPost
import asyncio


# asyncio.run(
# Service.AddPostToIndex(FullPost(
#     id=1,
#     title="ZOV",
#     text="ouoquwpeoupopquwe",
#     created_at= datetime.now(),
#     author_id=1,
#     author_name="Altair"
# ))
# )


async def qwe():
    res = await Service.SearchPost(
        "zov", 
        sort=[
            {"created_at": {"order": "desc"}}  # Сортировка по дате создания (новые сначала)
        ],
        page=1
    )   
    print(res)

asyncio.run(qwe())
