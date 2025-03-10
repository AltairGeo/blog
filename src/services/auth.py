import exceptions
import exceptions.users
import schemas
import security
from models.models import UsersModel
from repositories.users import UsersRepository


class AuthService:
    def __init__(self, users_repo: UsersRepository) -> schemas.token.Token:
        self.users_repo: UsersRepository = users_repo()

    async def Register(self, user: schemas.users.RegisterSchema) -> schemas.token.Token:
        """
        Registration.
        """
        user_dict = user.model_dump()  # From pydantic schema to dictionary
        user_found = await self.users_repo.find_one(email=user.email)
        if user_found:  # If user exists throw error
            raise exceptions.users.UserAlreadyCreate

        user_dict["password"] = security.utils.create_hash(user_dict["password"])  # Hashing password
        resp: UsersModel = await self.users_repo.create(user_dict)
        user_schema = resp.to_schema()
        return security.utils.token_from_user_schema(
            schema=user_schema
        )

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
            return security.utils.token_from_user_schema(user)
        else:
            raise exceptions.users.UncorrectEmailOrPassword
