from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    APP_NAME: str = "AI Medical Assistant"
    DEBUG: bool = True

    DATABASE_URL: str = ""

    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "medical_docs"
    VECTOR_SIZE: int = 786

    # Google Embeddings
    GEMINI_API_KEY: str = ""

    # Ollama
    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = ""

    # JWT
    JWT_SECRET_KEY: str = ""
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_EXPIRE_DAYS: int = 7

    #Pipeline
    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50

    UPLOAD_DIR: str = "uploads"

    model_config = SettingsConfigDict(env_file=".env")


config = Config()
