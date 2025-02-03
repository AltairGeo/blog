import exceptions.users
from repositories.users import UsersRepository
import schemas
import exceptions
import security
import security.token
import security.utils
from models.users import UsersModel
from settings import AppSettings
from datetime import datetime, timezone, timedelta

class AuthService:
    def __init__(self, users_repo: UsersRepository) -> schemas.token.Token:
        self.users_repo: UsersRepository = users_repo()

    async def Register(self, user: schemas.users.RegisterSchema) -> schemas.token.Token:
        """
        Registration.
        """
        user_dict = user.model_dump() # From pydantic schema to dictionary
        user_found = await self.users_repo.find_one(email=user.email)
        if user_found: # If user exists throw error
            raise exceptions.users.UserAlreadyCreate
        
        user_dict["password"] = security.utils.create_hash(user_dict["password"]) # Hashing password
        resp: UsersModel  = await self.users_repo.create(user_dict)
        user_schema = resp.to_schema()
        return security.token.generate_jwt_token(
            schemas.token.TokenData(
                id=user_schema.id,
                email=user_schema.email,
                expires_at= (datetime.now(timezone.utc) + timedelta(hours=AppSettings.token_life_time)).isoformat() # Time to expire token
            )
        )
        
    async def Login(self, data: schemas.users.LoginSchema) -> schemas.token.Token:
        ...

        