import dotenv
from os import getenv
from typing import List

dotenv.load_dotenv()

class Settings:
    def __init__(self):
        # Получение секретов из переменной среды
        self.jwt_secret = getenv("JWT_SECRET")
        self.db_url= getenv("DB_URL") # databaseName+driver://user:password@ip:port/db
                                      # postgresql+asyncpg://user:password@ip:port/db 
        
        self.jwt_algo: List[str]  = ["HS256"]
        self.token_life_time: int = 5 # In hours

AppSettings = Settings()