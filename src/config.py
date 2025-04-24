from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_NAME: str

    @property
    def base_url(self):
        return f"postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

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
        env_file=BASE_DIR / '.env',
        env_file_encoding='utf-8',
    )


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / 'certificates' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certificates' / 'jwt-public.pem'
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 30


settings = Settings()
auth_jwt: AuthJWT = AuthJWT()
