from config import settings
import hashlib
from random import randint
import schemas
import os



class IndexationImage:
    def __init__(self):
        self.__fraction_ratio = settings.fraction_ratio

    def create_index(self) -> str:
        print(self.__fraction_ratio)
        folder_frac = randint(1, int(self.__fraction_ratio))
        print(folder_frac)
        return hashlib.md5(str(folder_frac).encode()).hexdigest()
    
    def create_hash(self, inp: schemas.AvatarHashGenerate) -> str:
        pre = f"{str(inp.id)}{inp.email}"
        res = hashlib.md5(pre.encode()).hexdigest()
        return res

    def compose_hashs(self, in_dex: str, hashs: str) -> str:
        return f"{in_dex}@{hashs}"


class ImageFS(IndexationImage):
    def __init__(self):
        super().__init__()
        self.__def_path = settings.img_storage_path

    def AvatarSave(self, inp: schemas.AvatarHashGenerate, image):
        if not os.path.exists(self.__def_path):
            os.mkdir(self.__def_path)
        index = self.create_index()
        if not os.path.exists(f"{self.__def_path}/{index}"):
            os.mkdir(f"{self.__def_path}/{index}")

        image_hash = self.create_hash(inp)
        with open(f"{self.__def_path}/{index}/{image_hash}.png", "wb") as f:
            f.write(image)


        


    