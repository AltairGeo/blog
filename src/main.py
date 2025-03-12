import uvicorn
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import all_routers


logging.basicConfig(
    format="[{levelname}]=[{asctime}]==> {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
    filename='main.log',
    filemode="a",
    encoding="utf-8",
)


app = FastAPI(
    title="BlogAPI",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in all_routers:
    app.include_router(router=router)

if __name__ == "__main__":
    logging.info("Starting application!")
    uvicorn.run(app="main:app", reload=True)
