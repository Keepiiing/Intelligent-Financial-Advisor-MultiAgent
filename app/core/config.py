from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Smart Financial Advisor"
    environment: str = "local"
    api_prefix: str = "/api/v1"
    use_sample_data: bool = True
    default_fx_limit_usd: float = 50000.0
    usd_cny_rate: float = 7.20
    data_dir: Path = Path(__file__).resolve().parents[2] / "data"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
