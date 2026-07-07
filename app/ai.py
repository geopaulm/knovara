from __future__ import annotations

from typing import Protocol

import httpx

from app.config import Settings


class AIService(Protocol):
    def embed(self, texts: list[str]) -> list[list[float]]:
        pass


class OpenAIEmbeddingService:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def embed(self, texts: list[str]) -> list[list[float]]:
        if not self.settings.ai_api_key:
            raise ValueError("AI_API_KEY is required")

        response = httpx.post(
            f"{self.settings.ai_base_url.rstrip('/')}/embeddings",
            headers={"Authorization": f"Bearer {self.settings.ai_api_key}"},
            json={"model": self.settings.ai_embedding_model, "input": texts},
            timeout=30,
        )
        response.raise_for_status()
        return [item["embedding"] for item in response.json()["data"]]
