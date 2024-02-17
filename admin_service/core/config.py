from functools import lru_cache

from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file_encoding="utf-8")

    # JWT
    API_V1_STR: str = "/api/v1"
    JWT_SECRET: str = "TEST_SECRET_DO_NOT_USE_IN_PROD"
    ALGORITHM: str = "HS256"

    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

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

    # RabbitMQ
    rabbitmq_user: str = "guest"
    rabbitmq_password: SecretStr = SecretStr("guest")
    rabbitmq_host: str = "localhost"
    rabbitmq_port: int = 5672
    rabbitmq_vhost: str = "/"
    rabbitmq_queue: str = "email_queue"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
