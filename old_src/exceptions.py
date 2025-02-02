from fastapi import HTTPException


class TokenWasExpire(HTTPException):
    def __init__(self):
        super().__init__(418, "Token was expired!")

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

class InvalidID(HTTPException):
    def __init__(self):
        super().__init__(400, "ID lower or is zero!")

class PostNotFound(HTTPException):
    def __init__(self):
        super().__init__(404, detail="Post not found 0_o!")

class IsNotYourPost(HTTPException):
    def __init__(self):
        super().__init__(400, detail="Is not your post!")