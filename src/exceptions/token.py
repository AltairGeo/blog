from exceptions.base import Base


class DecodingWasFailed(Base):
    def __init__(self):
        super().__init__(500, "Token decoding was failed!")


class CreationTokenWasFailed(Base):
    def __init__(self):
        super().__init__(500, "Creation token was failed!")


class TokenWasExpired(Base):
    def __init__(self):
        super().__init__(400, "Token was expire! :(")
