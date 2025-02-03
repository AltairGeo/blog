from exceptions.base import Base

class UserAlreadyCreate(Base):
    def __init__(self):
        super().__init__(400, "User has already created!")

class UserNotFound(Base):
    def __init__(self):
        super().__init__(400, "User not found 0_o!")

class UncorrectEmailOrPassword(Base):
    def __init__(self):
        super().__init__(400, "Incorrect email or password!")