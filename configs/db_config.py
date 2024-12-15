from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://user:password@localhost/dbname"
    SECRET_KEY: str = "dq8k2j3m4n5p7r8t9v2x4z6b9c3f5h7k9m2n4p6q8s"

    class Config:
        env_file = ".env"


settings = Settings()