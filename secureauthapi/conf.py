from functools import lru_cache
from pathlib import Path
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class SecureAuthAPISettings(BaseSettings):
    JWT_SECRET: str = "your_default_jwt_secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = 30

    I18N_LOCALES_DIR: str = str(Path(__file__).resolve().parent / "locales")
    I18N_DEFAULT_LANGUAGE: str = "en"
    I18N_DOMAIN: str = "messages"

    LOGIN_ATTEMPTS_ENABLED: bool = False
    LOGIN_ATTEMPTS_MAX: int = 5


@lru_cache
def get_settings():
    return SecureAuthAPISettings()
