import os
from dataclasses import dataclass
from functools import lru_cache

DEFAULT_DATABASE_URL = "postgresql+psycopg://documind:documind@localhost:5432/documind"
DEFAULT_DOCUMENT_STORAGE_DIR = "storage/documents"


@dataclass(frozen=True)
class Settings:
    database_url: str
    document_storage_dir: str = DEFAULT_DOCUMENT_STORAGE_DIR


@lru_cache
def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL),
        document_storage_dir=os.getenv("DOCUMENT_STORAGE_DIR", DEFAULT_DOCUMENT_STORAGE_DIR),
    )
