from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    app_name: str = Field(..., env="APP_NAME")
    app_version: str = Field(..., env="APP_VERSION")
    debug: bool = Field(..., env="DEBUG")
    max_orders_per_day: int = Field(..., env="MAX_ORDERS_PER_DAY")
    maintenance_mode: bool = Field(..., env="MAINTENANCE_MODE")
    

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()