from repositories.users import UsersRepository
from services.users import UsersService
from services.auth import AuthService

def users_service():
    return UsersService(UsersRepository)

def auth_service():
    return AuthService(UsersRepository)