from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from api.routers import all_routers
from elasticsearch import AsyncElasticsearch
from settings import AppSettings

app = FastAPI(
    title="BlogAPI"
)
es = AsyncElasticsearch(
    AppSettings.elastic_host,
    basic_auth=(AppSettings.elastic_user, AppSettings.elastic_password),
    verify_certs=False
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def check_elastic():
    if not await es.ping():
        raise HTTPException(500, "Elastic is not available!")


@app.on_event("shutdown")
async def disconnect_elastic():
    await es.close()

for router in all_routers:
    app.include_router(router=router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)