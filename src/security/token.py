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
        print(to_encode)
        encoded_jwt = jwt.encode(to_encode, AppSettings.jwt_secret, AppSettings.jwt_algo[0])
        return encoded_jwt
    except Exception as e:
        logging.error(str(e))
        raise exceptions.token.CreationTokenWasFailed


def decode_jwt_token(token: Token) -> TokenData:
    try:
        return jwt.decode(token.token, AppSettings.jwt_secret, AppSettings.jwt_algo)
    except Exception as e:
        logging.error(str(e))
        raise exceptions.token.DecodingWasFailed


def check_token_to_expire(token: Token):
    decoded = decode_jwt_token(token=token)
    if datetime.fromisoformat(decoded.expires_at) > datetime.now(timezone.utc):
        return True
    else:
        raise exceptions.token.TokenWasExpired
