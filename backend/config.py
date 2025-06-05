from __future__ import annotations

from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    data_dir: Path = Path(__file__).parent / ".." / "data"


settings = Settings()
