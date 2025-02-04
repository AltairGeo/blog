import dotenv
from os import getenv
from typing import List

dotenv.load_dotenv()

class Settings:
    def __init__(self):
        # Получение секретов из переменной среды
        self.jwt_secret = getenv("JWT_SECRET")
        self.db_url = getenv("DB_URL") # databaseName+driver://user:password@ip:port/db
                                      # postgresql+asyncpg://user:password@ip:port/db 

        self.s3accesKey: str = getenv("S3_ACCESS_KEY_ID") # s3 storage access keys
        self.s3secretKey: str = getenv("S3_SECRET_ACCESS_KEY")
        self.s3endpointurl: str = getenv("S3_endpoint_url") # s3 url
        self.bucket_name = getenv("bucket_name")
        
        self.jwt_algo: List[str]  = ["HS256"]
        self.token_life_time: int = 5 # In hours

AppSettings = Settings()