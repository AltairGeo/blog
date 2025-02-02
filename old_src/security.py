import hashlib
import jwt
import schemas
from config import settings
from datetime import datetime, timezone
import exceptions

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
        return schemas.Token(token=jwt.encode({"id": user.id, "email": user.email, "expires_at": user.expires_at.isoformat()},
                                               settings.jwt_secret, 
                                               settings.jwt_algo[0]))


    @staticmethod
    def decodeJWT(token: schemas.Token) -> schemas.UserFToken:
        try:
            decoded = jwt.decode(token.token, settings.jwt_secret, algorithms=settings.jwt_algo)
            return schemas.UserFToken(id=decoded["id"],
                                    email=decoded["email"],
                                    expires_at=datetime.fromisoformat(decoded["expires_at"]))
        except:
            raise exceptions.InvalidToken


    @staticmethod
    def check_token_for_expire(token: schemas.Token):
        decoded = JwT.decodeJWT(token=token)
        if decoded.expires_at > datetime.now(timezone.utc):
            return True
        else:
            return False
        
    @staticmethod
    def check_for_expire(date: datetime):
        if date > datetime.now(timezone.utc):
            return True
        else:
            return False
