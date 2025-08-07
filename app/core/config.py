from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # TODO: Replace with actual database credentials
    DATABASE_URL: str = "postgresql://user:password@localhost/e_commerce_db"

    # Secret key for signing JWTs
    SECRET_KEY: str = "a_very_secret_key_that_should_be_changed"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        # This allows loading variables from a .env file
        env_file = ".env"
        env_file_encoding = 'utf-8'

settings = Settings()
