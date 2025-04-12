import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def base_url(self):
        return  f"postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    @property
    def naming_convention(self):
        return {
                  "ix": "ix_%(column_0_label)s",
                  "uq": "uq_%(table_name)s_%(column_0_name)s",
                  "ck": "ck_%(table_name)s_%(constraint_name)s",
                  "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
                  "pk": "pk_%(table_name)s"
                }

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=os.path.join(os.path.dirname(__file__), '..', '.env'),
        env_file_encoding='utf-8',
    )

settings = Settings()
