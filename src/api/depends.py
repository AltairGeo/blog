from repositories.users import UsersRepository
from repositories.posts import PostsRepository
from services.users import UsersService
from services.auth import AuthService
from services.posts import PostsService

def users_service():
    return UsersService(UsersRepository)

def auth_service():
    return AuthService(UsersRepository)

def posts_service():
    return PostsService(PostsRepository)