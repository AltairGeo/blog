import dotenv
import os

dotenv.load_dotenv()

class Settings:
    jwt_secret: str = os.getenv("JWT_SECRET")
    jwt_algo = ["HS256"]


settings = Settings()