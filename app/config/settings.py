

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    GEMINI_API_KEY: str

    GEMINI_MODEL: str

    QDRANT_URL: str

    QDRANT_API_KEY: str = ""

    COLLECTION_NAME: str

    EMBEDDING_MODEL: str

    REDIS_HOST: str

    REDIS_PORT: int

    REDIS_PASSWORD: str = ""

    CHUNK_SIZE: int

    CHUNK_OVERLAP: int

    class Config:
        env_file = ".env"


settings = Settings()