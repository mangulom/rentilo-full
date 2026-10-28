from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Rentilo"
    database_url: str = "postgresql+psycopg2://postgres:CAMBIAR_CLAVE@localhost:15432/rentilo"
    secret_key: str = "replace-this-development-secret"
    cors_origins: list[str] = ["http://localhost:4200"]
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
