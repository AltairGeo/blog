from repositories.alchemy_repo import SQLAlchemyRepository
from models.models import UsersModel

class UsersRepository(SQLAlchemyRepository):
    model = UsersModel

