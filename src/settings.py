from os import getenv
from typing import List

import dotenv
from pydantic import HttpUrl, Field

dotenv.load_dotenv()


class Settings:
    def __init__(self):
        # Получение секретов из переменных окружения и .env
        self.jwt_secret: Field(min_length=10) = getenv("JWT_SECRET")
        self.db_url: str = getenv("DB_URL")  # databaseName+driver://user:password@ip:port/db
        # postgresql+asyncpg://user:password@ip:port/db

        self.s3accesKey: str = getenv("S3_ACCESS_KEY_ID")  # s3 storage access keys
        self.s3secretKey: str = getenv("S3_SECRET_ACCESS_KEY")
        self.s3endpointurl: HttpUrl = getenv("S3_endpoint_url")  # s3 url
        self.bucket_name: str = getenv("bucket_name")

        self.elastic_host: HttpUrl = getenv("ELASTIC_HOST")
        self.elastic_user: str = getenv("ELASTIC_USER")
        self.elastic_password: str = getenv("ELASTIC_PASSWORD")

        self.jwt_algo: List[str] = ["HS256"]
        self.token_life_time: int = 120  # In minutes


AppSettings = Settings()
