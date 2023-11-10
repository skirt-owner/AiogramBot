__all__ = ["config"]

import os

from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    telegram_token: SecretStr
    admins: str

    postgres_username: str
    postgres_password: SecretStr
    postgres_host: SecretStr
    postgres_port: int
    postgres_database: str

    redis_host: SecretStr
    redis_user: str
    redis_password: SecretStr

    class Config:
        env_file = '.venv'
        env_file_encoding = 'utf-8'


config = Settings()
