import exceptions.users
from repositories.users import UsersRepository
import schemas.users as users
import exceptions

class UsersService:
    def __init__(self, users_repo: UsersRepository):
        self.users_repo: UsersRepository = users_repo()

    async def AddNewUser(self, user: users.UserAddSchema) -> int:
        user_dict = user.model_dump()
        user_found = await self.users_repo.find_one(email=user.email)
        if user_found:
            raise exceptions.users.UserAlreadyCreate
        
        user_id = await self.users_repo.create(data=user_dict)
        return user_id

    async def GetAllUsers(self):
        users = await self.users_repo.find_all()
        return users