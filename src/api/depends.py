import asyncio
from typing import Annotated

from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from repositories.elastic import ElasticRepo
from repositories.likes import LikesRepository
from repositories.posts import PostsRepository
from repositories.s3 import S3Repo
from repositories.users import UsersRepository
from services.auth import AuthService
from services.elastic import ElasticService
from services.likes import LikesService
from services.posts import PostsService
from services.s3 import S3Service
from services.users import UsersService
from settings import AppSettings

oauth_schema = OAuth2PasswordBearer(tokenUrl="/auth/login")


def users_service():
    return UsersService(UsersRepository)


def auth_service():
    return AuthService(UsersRepository)


def posts_service():
    return PostsService(PostsRepository)


def elastic_service():
    return ElasticService(
        elastic_repo=ElasticRepo(
            es_client=AsyncElasticsearch(
                AppSettings.elastic_host,
                basic_auth=(AppSettings.elastic_user, AppSettings.elastic_password),
                verify_certs=False
            ),
            index_name="posts"
        ),
        posts_repo=PostsRepository
    )


def s3_service():
    return S3Service(S3Repo(
        access_key=AppSettings.s3accesKey,
        secret_key=AppSettings.s3secretKey,
        bucket_name=AppSettings.bucket_name,
        endpoint_url=AppSettings.s3endpointurl,
    ),
        UsersRepository()
    )


async def get_current_user(
        token: Annotated[str, Depends(oauth_schema)],
        serv_auth: Annotated[AuthService, Depends(auth_service)]
):
    return await serv_auth.GetUserWithToken(token)


def likes_service():
    return LikesService(likes_repo=LikesRepository)