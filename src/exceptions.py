from fastapi import HTTPException


class TokenWasExpire(HTTPException):
    def __init__(self):
        super().__init__("Token was expired!")
        self.status_code = 418


class PageLessZero(HTTPException):
    def __init__(self):
        super().__init__(400, detail="The page less zero!")


class PostsNotFound(HTTPException):
    def __init__(self):
        super().__init__(404, detail="Posts not found 0_o!")


class InvalidToken(HTTPException):
    def __init__(self):
        super().__init__(400, detail="Invalid token! Decoding was failed!")


class UserNotFound(HTTPException):
    def __init__(self):
        super().__init__(404, detail="User not found 0_o!")