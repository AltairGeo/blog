import logging
from contextlib import asynccontextmanager

from aiobotocore.session import get_session


class S3Repo():
    def __init__(
            self,
            access_key: str,
            secret_key: str,
            endpoint_url: str,
            bucket_name: str,
    ):
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
        }

        self.bucket_name = bucket_name
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        try:
            async with self.session.create_client("s3", **self.config) as client:
                yield client
        except Exception as e:
            logging.error(e)
            raise e

    async def upload_avatar(self, key: str, file: bytes) -> str:
        try:
            async with self.get_client() as client:
                await client.put_object(
                    Bucket=self.bucket_name,
                    Key=key,
                    Body=file,
                    ContentType="image/jpeg",
                )
                return await self.compose_path(key=key)
        except Exception as e:
            logging.error(str(e))
            raise e

    async def compose_path(self, key: int) -> str:
        try:
            return f"{self.config["endpoint_url"]}{self.bucket_name}/{key}"
        except Exception as e:
            logging.error(e)
            raise e
