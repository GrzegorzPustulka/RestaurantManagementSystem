from functools import lru_cache

from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file_encoding="utf-8")

    # DATABASE
    POSTGRES_USER: str = "postgres"
    PGPASSWORD: SecretStr = SecretStr("SecretPassword_1!")
    PGHOST: str = "localhost"
    PGPORT: str = "5432"
    PGDATABASE: str = "DineStream"

    @property
    def sqlalchemy_database_uri(self) -> PostgresDsn:
        return f"postgresql://{self.POSTGRES_USER}:{self.PGPASSWORD.get_secret_value()}@{self.PGHOST}:{self.PGPORT}/{self.PGDATABASE}"

    # SMTP
    smtp_server: str = "localhost"
    smtp_port: int = 1025
    sender_email: str = "test@example.com"
    smtp_password: SecretStr = SecretStr("")


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
