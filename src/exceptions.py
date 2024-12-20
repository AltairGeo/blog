from fastapi import HTTPException


class TokenWasExpire(HTTPException):
    def __init__(self):
        super().__init__("Token was expired!")
        self.status_code = 418