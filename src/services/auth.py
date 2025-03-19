import exceptions
import exceptions.users
import schemas
import security
from models.models import UsersModel
from repositories.users import UsersRepository


class AuthService:
    def __init__(self, users_repo: UsersRepository):
        self.users_repo: UsersRepository = users_repo()

    async def Register(self, user: schemas.users.RegisterSchema):
        """
        Registration.
        """
        user_found = await self.users_repo.find_one(email=user.email)
        if user_found:
            raise exceptions.users.UserAlreadyCreate

        user.password = security.utils.create_hash(user.password)  # Hashing password
        user_dict = user.model_dump()
        resp: UsersModel = await self.users_repo.create(user_dict)
        user_schema = resp.to_schema()
        return user_schema

    async def Login(self, data: schemas.users.LoginSchema) -> schemas.token.Token:
        """
        Login.
        """
        user: UsersModel = await self.users_repo.find_one(email=data.email)
        if not user:
            raise exceptions.users.UserNotFound
        hash_pass = security.utils.create_hash(data.password)
        user = user.to_schema()

        if user.password == hash_pass:
            token_str = security.token.create_access_token(data={"id": user.id, "email": user.email})
            return schemas.token.Token(
                access_token=token_str,
                token_type="bearer",
            )
        else:
            raise exceptions.users.UncorrectEmailOrPassword

    async def GetUserWithToken(self, token: str) -> schemas.tables.UsersSchema:
        """
        Getting user by token.
        """
        tokenData = security.token.decode_jwt_token(token)
        user: UsersModel = await self.users_repo.find_one(email=tokenData.email, id=tokenData.id)
        if user is None:
            raise exceptions.users.UserNotFound
        return user.to_schema()