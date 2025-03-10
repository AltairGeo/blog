from api.auth import router as auth
from api.posts import router as posts
from api.search import router as search
from api.users import router as users

all_routers = [
    users,
    auth,
    posts,
    search
]
