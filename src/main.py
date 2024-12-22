from fastapi import FastAPI
import routers
import uvicorn
from fastapi.responses import HTMLResponse


app = FastAPI()

app.include_router(routers.posts.router)
app.include_router(routers.users.router)

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
            <h1>Blog API</h1>
            <p><a href="/docs">Please enter to swagger docs!</a></p>
           """


if __name__ == "__main__":
    uvicorn.run(app=app)