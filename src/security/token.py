import logging
from datetime import datetime, timezone, timedelta
import jwt

import exceptions
import exceptions.token
from schemas.token import Token, TokenData
from settings import AppSettings


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=AppSettings.token_life_time)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, AppSettings.jwt_secret, AppSettings.jwt_algo[0])
        return encoded_jwt
    except Exception as e:
        logging.error(str(e))
        raise exceptions.token.CreationTokenWasFailed


def decode_jwt_token(token: str) -> TokenData:
    try:
        decoded: dict = jwt.decode(token, AppSettings.jwt_secret, AppSettings.jwt_algo)
        if decoded.get("id") is None or decoded.get("email") is None:
            raise exceptions.token.DecodingWasFailed
        return TokenData(id=decoded["id"], email=decoded["email"])

    except Exception as e:
        logging.error(str(e))
        raise exceptions.token.DecodingWasFailed


def check_token_to_expire(token: Token):
    decoded = decode_jwt_token(token=token)
    if datetime.fromisoformat(decoded.expires_at) > datetime.now(timezone.utc):
        return True
    else:
        raise exceptions.token.TokenWasExpired
