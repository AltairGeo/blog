from datetime import datetime, timezone

import jwt

import exceptions
import exceptions.token
from schemas.token import Token, TokenData
from settings import AppSettings


def generate_jwt_token(data: TokenData) -> Token:
    try:
        return Token(
            token=jwt.encode(
                data.model_dump(),
                AppSettings.jwt_secret,
                AppSettings.jwt_algo[0],
            )
        )
    except Exception as e:
        print(e)
        raise exceptions.token.DecodingWasFailed


def decode_jwt_token(token: Token) -> TokenData:
    try:
        decode = jwt.decode(token.token, AppSettings.jwt_secret, AppSettings.jwt_algo)
        return TokenData(
            id=decode["id"],
            email=decode["email"],
            expires_at=decode["expires_at"]
        )
    except Exception as e:
        print(e)
        raise exceptions.token.DecodingWasFailed


def check_token_to_expire(token: Token):
    decoded = decode_jwt_token(token=token)
    if datetime.fromisoformat(decoded.expires_at) > datetime.now(timezone.utc):
        return True
    else:
        raise exceptions.token.TokenWasExpired
