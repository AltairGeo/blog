from repositories.users import UsersRepository
from repositories.posts import PostsRepository
from services.users import UsersService
from services.auth import AuthService
from services.posts import PostsService
from services.s3 import S3Service
from repositories.s3 import S3Repo
from settings import AppSettings

def users_service():
    return UsersService(UsersRepository)

def auth_service():
    return AuthService(UsersRepository)

def posts_service():
    return PostsService(PostsRepository)

def s3_service():
    return S3Service(S3Repo(
        access_key=AppSettings.s3accesKey,
        secret_key=AppSettings.s3secretKey,
        bucket_name=AppSettings.bucket_name,
        endpoint_url=AppSettings.s3endpointurl,
    ),
    UsersRepository()
    )