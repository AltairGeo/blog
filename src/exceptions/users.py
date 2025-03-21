from fastapi import status, HTTPException

from exceptions.base import Base


class UserAlreadyCreate(Base):
    def __init__(self):
        super().__init__(400, "User has already created!")


class UserNotFound(Base):
    def __init__(self):
        super().__init__(404, "User not found 0_o!")


class UncorrectEmailOrPassword(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"})


class SamePasswords(Base):
    def __init__(self):
        super().__init__(400, "You specified the same passwords")


class AvatarNotFound(Base):
    def __init__(self):
        super().__init__(404, "Avatar not found 0_o!")
