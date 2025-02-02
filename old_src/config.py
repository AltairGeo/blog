import dotenv
import os
from configparser import ConfigParser
import os


dotenv.load_dotenv()

if not os.path.exists("./config/"): # Создание директории если таковая отсутствует
    os.mkdir("./config/") 

if not os.path.exists("./config/fs.ini"): # Создание дефолтного конфига если такой отсутствует
    conf = ConfigParser()
    conf['AVATAR_STORAGE'] = {"path": "./imgsFS",
                              "fraction_ratio": 5}
    
    with open("./config/fs.ini", "w") as cnf:
        conf.write(cnf)


class Settings:    
    def __init__(self):
        # Получение секретов из переменной среды
        self.jwt_secret = os.getenv("JWT_SECRET")
        self.jwt_algo = ["HS256"]
        self.db_url= os.getenv("DB_URL") # user:password@ip:port/db 
        # postgresql+asyncpg://user:password@ip:port/db

        # Чтение конфига и получение настроек
        conf = ConfigParser()
        conf.read("./config/fs.ini")
        self.img_storage_path = conf['AVATAR_STORAGE']['path']
        self.fraction_ratio = conf['AVATAR_STORAGE']['fraction_ratio']



settings = Settings()