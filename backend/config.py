import sys
import pathlib
import logging
from pydantic import BaseModel, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import create_engine
from config_utils import load_yaml
from db import set_new_engine

path = pathlib.Path(__file__).parent.resolve()


def setup_logging():
    logging.basicConfig(stream=sys.stdout, level=Config.verbosity, force=True)


def setup_engine(db_uri: str | None = None):
    db_url = db_uri if db_uri else (Settings.TEST_DB_URI if Config.tests else Settings.DB_URI)
    set_new_engine(create_engine(url=db_url, echo=False))


env_file_path = pathlib.Path(__file__).parent.resolve() / ".env"


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_file_path,
        env_ignore_empty=True,
        extra="ignore",
    )
    DB_TYPE: str = "mssql"
    DB_DRIVER: str = "pyodbc"
    DB_USER: str = "username"
    DB_PASSWORD: str = "password"
    DB_SERVER: str | None = "localhost"
    DB_DB: str = "db"
    DB_SYSTEM_DRIVER: str = "ODBC+Driver+17+for+SQL+Server"

    TEST_DB_PASSWORD: str = "password"
    TEST_DB_DB: str = "test_db"

    TEST_DB_MASTER: str = "master"

    @computed_field
    @property
    def DB_URI(self) -> str:
        return (
            f"{self.DB_TYPE}+{self.DB_DRIVER}://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_SERVER}/{self.DB_DB}?"
            f"driver={self.DB_SYSTEM_DRIVER}"
        )

    @computed_field
    @property
    def TEST_DB_URI(self) -> str:
        return (
            f"{self.DB_TYPE}+{self.DB_DRIVER}://"
            f"{self.DB_USER}:{self.TEST_DB_PASSWORD}"
            f"@{self.DB_SERVER}/{self.TEST_DB_DB}?"
            f"driver={self.DB_SYSTEM_DRIVER}"
        )

    @computed_field
    @property
    def TEST_DB_MASTER_URI(self) -> str:
        return (
            f"{self.DB_TYPE}+{self.DB_DRIVER}://"
            f"{self.DB_USER}:{self.TEST_DB_PASSWORD}"
            f"@{self.DB_SERVER}/{self.TEST_DB_MASTER}?"
            f"driver={self.DB_SYSTEM_DRIVER}"
        )


class AppConfig(BaseModel):
    verbosity: str = 'INFO'
    tests: bool = False
    trends_writer: dict
    simulator: dict
    leak_detector: dict


app_config = load_yaml(path, "config.yaml")
Config = AppConfig(**app_config)
Settings = AppSettings()
setup_logging()
