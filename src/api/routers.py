from api.users import router as users
from api.auth import router as auth
from api.posts import router as posts

all_routers = [
    users,
    auth,
    posts
    ]