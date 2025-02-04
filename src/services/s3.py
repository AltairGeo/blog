from repositories.s3 import S3Repo
from repositories.users import UsersRepository
import security
import schemas


class S3Service:
    def __init__(self, s3repo: S3Repo, user_repo: UsersRepository):
        self.s3_repo: S3Repo = s3repo
        self.users_repo: UsersRepository = UsersRepository()

    async def UploadAvatar(self, data: schemas.users.AvatarUpload) -> str:
        security.token.check_token_to_expire(token=data.token) # check token to expire
        decoded = security.token.decode_jwt_token(token=data.token) # decode token
        resp: str = await self.s3_repo.upload_avatar(key=str(decoded.id), file=data.file) # Upload avatar to s3
        goida = await self.users_repo.update({"avatar_path": resp}, id=decoded.id, email=decoded.email)
        return resp
        
    
