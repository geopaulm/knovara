import os
from dataclasses import dataclass
from functools import lru_cache

DEFAULT_DATABASE_URL = "postgresql+psycopg://documind:documind@localhost:5432/documind"
DEFAULT_DOCUMENT_STORAGE_DIR = "storage/documents"
DEFAULT_AI_BASE_URL = "https://api.openai.com/v1"
DEFAULT_AI_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_AI_CHAT_MODEL = "gpt-4o-mini"


@dataclass(frozen=True)
class Settings:
    database_url: str
    document_storage_dir: str = DEFAULT_DOCUMENT_STORAGE_DIR
    ai_api_key: str = ""
    ai_base_url: str = DEFAULT_AI_BASE_URL
    ai_embedding_model: str = DEFAULT_AI_EMBEDDING_MODEL
    ai_chat_model: str = DEFAULT_AI_CHAT_MODEL


@lru_cache
def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL),
        document_storage_dir=os.getenv("DOCUMENT_STORAGE_DIR", DEFAULT_DOCUMENT_STORAGE_DIR),
        ai_api_key=os.getenv("AI_API_KEY", ""),
        ai_base_url=os.getenv("AI_BASE_URL", DEFAULT_AI_BASE_URL),
        ai_embedding_model=os.getenv("AI_EMBEDDING_MODEL", DEFAULT_AI_EMBEDDING_MODEL),
        ai_chat_model=os.getenv("AI_CHAT_MODEL", DEFAULT_AI_CHAT_MODEL),
    )
