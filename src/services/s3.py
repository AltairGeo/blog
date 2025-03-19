import schemas
import security
from repositories.s3 import S3Repo
from repositories.users import UsersRepository
from schemas.tables import UsersSchema


class S3Service:
    def __init__(self, s3repo: S3Repo, user_repo: UsersRepository):
        self.s3_repo: S3Repo = s3repo
        self.users_repo: UsersRepository = UsersRepository()

    async def UploadAvatar(self, file: bytes, usr: UsersSchema) -> str:
        resp: str = await self.s3_repo.upload_avatar(key=str(usr.id), file=file)  # Upload avatar to s3
        update = await self.users_repo.update({"avatar_path": resp}, id=usr.id, email=usr.email)
        return resp

