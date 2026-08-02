"""Agent settings."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # AI APIs
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    google_ai_api_key: str = ""
    tavily_api_key: str = ""

    # Backend
    backend_api_url: str = "http://localhost:8000/api/v1"
    backend_api_key: str = ""

    # Agent config
    n_runs_per_prompt: int = 3
    stability_threshold: float = 0.7
    enable_hitl_sentiment: bool = True
    enable_hitl_hallucination: bool = True

    # LiteLLM model mapping
    model_map: dict[str, str] = {
        "chatgpt-mini": "gpt-4o-mini",
        "chatgpt": "gpt-4o",
        "claude-haiku": "claude-3-5-haiku-20241022",
        "claude-sonnet": "claude-3-5-sonnet-20241022",
        "gemini-flash": "gemini/gemini-1.5-flash",
        "gemini-pro": "gemini/gemini-1.5-pro",
    }


settings = Settings()
