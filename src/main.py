from fastapi import FastAPI
from routers import users
from routers import posts
import uvicorn

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)

if __name__ == "__main__":
    uvicorn.run(app=app)