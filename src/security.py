import hashlib
import jwt
import schemas
from config import settings
from jwt.exceptions import InvalidSignatureError


class Hashing:
    @staticmethod
    def create_hash(password: str) -> str:
        if not isinstance(password, str):
            raise ValueError("Password must be a string")
        if not password:
            raise ValueError("Password cannot be empty")
        hashs = hashlib.md5(password.encode()).hexdigest()
        return hashs
        

class JwT:
    @staticmethod
    def generateJWT(user: schemas.UserFToken) -> schemas.Token:
        return schemas.Token(token=jwt.encode({"id": user.id, "email": user.email}, settings.jwt_secret, settings.jwt_algo[0]))
    
    @staticmethod
    def decodeJWT(token: schemas.Token) -> schemas.UserFToken:
        decoded = jwt.decode(token.token, settings.jwt_secret, algorithms=settings.jwt_algo)
        return schemas.UserFToken(id=decoded["id"], email=decoded["email"])
        
