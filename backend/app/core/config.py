from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "LeaseLens API"
    environment: str = "development"
    database_url: str
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"
    api_v1_prefix: str = "/api/v1"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
