from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str
    app_version: str
    debug: bool
    max_orders_per_day: int
    maintenance_mode: bool

    class Config:
        model_config = SettingsConfigDict(env_file=".env")

# Inisialisasi settings
settings = Settings()
