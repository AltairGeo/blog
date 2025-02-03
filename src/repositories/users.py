from repositories.alchemy_repo import SQLAlchemyRepository
from models.users import UsersModel

class UsersRepository(SQLAlchemyRepository):
    model = UsersModel

