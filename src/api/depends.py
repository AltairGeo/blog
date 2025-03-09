from repositories.users import UsersRepository
from repositories.posts import PostsRepository
from repositories.elastic import ElasticRepo
from services.elastic import ElasticService
from services.users import UsersService
from services.auth import AuthService
from services.posts import PostsService
from services.s3 import S3Service
from repositories.s3 import S3Repo
from settings import AppSettings
from elasticsearch import AsyncElasticsearch

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