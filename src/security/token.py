import exceptions.token
from settings import AppSettings
import jwt
import exceptions
from schemas.token import Token, TokenData


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

    