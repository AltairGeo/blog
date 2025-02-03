from repositories.users import UsersRepository


class UsersService:
    def __init__(self, users_repo: UsersRepository):
        self.users_repo: UsersRepository = users_repo()

    async def GetAllUsers(self):
        """
        Get all users in db
        """
        users = await self.users_repo.find_all()
        return users