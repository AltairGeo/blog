from fastapi import FastAPI
from routers import users
from routers import posts
import uvicorn
from fastapi.responses import HTMLResponse


app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
            <h1>Blog API</h1>
            <p><a href="/docs">Please enter to swagger docs!</a></p>
           """


if __name__ == "__main__":
    uvicorn.run(app=app)