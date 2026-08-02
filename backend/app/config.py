"""Application settings — loaded from env vars."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Database
    database_url: str = "postgresql://geo:geo@localhost:5432/geo_ecom_dev"
    redis_url: str = "redis://localhost:6379/0"

    # AI APIs
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    google_ai_api_key: str = ""
    tavily_api_key: str = ""

    # App
    app_env: str = "development"
    log_level: str = "INFO"
    allowed_origins: list[str] = ["http://localhost:3000"]

    # Cost
    cost_budget_per_scan_usd: float = 0.30

    # Stability
    stability_threshold: float = 0.7
    n_runs_per_prompt: int = 3  # demo: 3, production: 7-8

    # Bootstrap CI
    bootstrap_iterations: int = 1000
    noise_floor_pct: float = 6.0  # 5-7 tuỳ paper

    # HITL
    enable_hitl_sentiment: bool = True
    enable_hitl_hallucination: bool = True


settings = Settings()
