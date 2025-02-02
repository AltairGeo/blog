from fastapi import FastAPI
import routers
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi.responses import HTMLResponse


app = FastAPI()

app.include_router(routers.posts.router)
app.include_router(routers.users.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def index():
    return """
            <h1>Blog API</h1>
            <p><a href="/docs">Please enter to swagger docs!</a></p>
           """


if __name__ == "__main__":
    uvicorn.run(app=app)
