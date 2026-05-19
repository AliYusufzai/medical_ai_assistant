from pydantic_settings import BaseSettings, SettingsConfigDict

class Config(BaseSettings):
    APP_NAME: str = 'AI Medical Assistant'
    DEBUG: bool = True

    DATABASE_URL: str

    # Qdrant
    QDRANT_URL: str = "http://localhost:6333"
    QDRANT_COLLECTION: str = "medical_docs"

    # Google Embeddings
    GOOGLE_API_KEY: str

    # Ollama
    OLLAMA_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.2:3b"

    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_EXPIRE_DAYS: int = 7

    model_config = SettingsConfigDict(env_file=".env")

config = Config()