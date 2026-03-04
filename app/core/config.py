"""
Application configuration.
"""

from pydantic_settings import BaseSettings
from functools import lru_cache

'''
LRU = Least Recently Used
It keeps recently used results in memory.
'''
class Settings(BaseSettings):
    # PostgreSQL settings
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432

    # Optional full database URL
    DATABASE_URL: str | None = None

    # JWT
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


    @property
    def database_url(self) -> str:
        """
        Return DATABASE_URL if provided,
        otherwise construct it from POSTGRES_* variables.
        """
        if self.DATABASE_URL:
            return self.DATABASE_URL

        return (
            f"postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}"
            f"/{self.POSTGRES_DB}"
        )



'''

🔹 Normal Method (Without @property)
class User:
    def get_name(self):
        return "Anushka"

u = User()
print(u.get_name())   # need parentheses

You must call it like a function:

u.get_name()
🔹 With @property
class User:
    @property
    def name(self):
        return "Anushka"

u = User()
print(u.name)   # no parentheses

Now it behaves like a variable:

u.name

But internally it is still a method.

'''

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()