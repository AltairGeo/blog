from config import settings
import hashlib
from random import randint
import schemas
import os
from PIL import Image
import io


class IndexationImage:
    def __init__(self):
        self.__fraction_ratio = settings.fraction_ratio

    def create_index(self) -> str:
        folder_frac = randint(1, int(self.__fraction_ratio))
        return hashlib.md5(str(folder_frac).encode()).hexdigest()
    
    def create_hash(self, inp: schemas.AvatarHashGenerate) -> str:
        pre = f"{str(inp.id)}{inp.email}"
        res = hashlib.md5(pre.encode()).hexdigest()
        return res

    def compose_hash(self, in_dex: str, hashs: str) -> str:
        return f"{in_dex}@{hashs}"
    
    def decompose_hash(self, image_hash: str):
        res = image_hash.split("@")
        return {"index": res[0], "hash": res[1]}


class ImageFS(IndexationImage):
    def __init__(self):
        super().__init__()
        self.__def_path = settings.img_storage_path

    def AvatarSave(self, inp: schemas.AvatarHashGenerate, image: bytes):
        index = self.create_index()
        if not os.path.exists(self.__def_path):
            os.mkdir(self.__def_path)
        if not os.path.exists(f"{self.__def_path}/{index}"):
            os.mkdir(f"{self.__def_path}/{index}")
        image_hash = self.create_hash(inp)

        buffer = io.BytesIO(image)
        buffer.seek(0)
        img = Image.open(buffer)
        left = (img.width - 256) // 2
        top = (img.height - 256) // 2
        right = left + 256
        bottom = top + 256
        img = img.crop((left, top, right, bottom))
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")

        with open(f"{self.__def_path}/{index}/{image_hash}.png", "wb") as f:
            f.write(buffer.getvalue())
        return self.compose_hash(index, image_hash)
    

    def DelOldAvatar(self, image_hash):
        dec = self.decompose_hash(image_hash)
        try:
            os.remove(f"{self.__def_path}/{dec["index"]}/{dec["hash"]}.png")
        except Exception as e:
            print(e)
            

    def OrganizePath(self, image_hash):
        dec = self.decompose_hash(image_hash)
        return f"{self.__def_path}/{dec["index"]}/{dec["hash"]}.png"
        


        


    