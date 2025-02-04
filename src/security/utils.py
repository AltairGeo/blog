import hashlib
import schemas
import security
from datetime import datetime, timezone, timedelta
from settings import AppSettings


def create_hash(password: str) -> str:
    if not isinstance(password, str):
        raise ValueError("Password must be a string")
    if not password:
        raise ValueError("Password cannot be empty")
    hashs = hashlib.md5(password.encode()).hexdigest()
    return hashs

def token_from_user_schema(schema: schemas.tables.UsersSchema):
    return security.token.generate_jwt_token(
            schemas.token.TokenData(
                id=schema.id,
                email=schema.email,
                expires_at= (datetime.now(timezone.utc) + timedelta(hours=AppSettings.token_life_time)).isoformat() # Time to expire token
            )
        )