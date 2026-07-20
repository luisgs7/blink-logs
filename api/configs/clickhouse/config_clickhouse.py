from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = None
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class GlobalConfig(BaseConfig):
    CLICKHOUSE_URL: Optional[str] = None


class DevConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_", env_file=".env", extra="ignore")


class ProdConfig(GlobalConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_", env_file=".env", extra="ignore")


class TestConfig(GlobalConfig):
    CLICKHOUSE_URL: str = "clickhouse://default@localhost:8123/blink_logs"
    model_config = SettingsConfigDict(env_prefix="TEST_", env_file=".env", extra="ignore")


@lru_cache()
def get_config(env_state: str):
    configs = {
        "dev": DevConfig,
        "prod": ProdConfig,
        "test": TestConfig,
    }
    return configs[env_state]()


config = get_config(BaseConfig().ENV_STATE)
