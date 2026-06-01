"""
Application settings loaded from environment variables.
Values are read from a .env file in development; set directly in staging/production.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
# import os

# from dotenv import load_dotenv

# load_dotenv()

# DATABASE_URL: str = os.environ["DATABASE_URL"]
# APP_ENV: str = os.getenv("APP_ENV", "development")


class Settings(BaseSettings):
    jwt_expiry_minutes: int
    jwt_secret: str
    jwt_algorithm: str
    database_url: str
    app_env: str = "development"
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
