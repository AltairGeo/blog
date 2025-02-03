from api.users import router as users
from api.auth import router as auth

all_routers = [
    users,
    auth]